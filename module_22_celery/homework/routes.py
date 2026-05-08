import os
import uuid
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from celery import group, chord
from celery.result import GroupResult
from celery import current_app
from tasks import process_single_image, make_archive_and_send_email
from models import subscribe, unsubscribe
from config import TEMP_FOLDER, ALLOWED_EXTENSIONS

api = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/blur', methods=['POST'])
def blur_images():
    if 'email' not in request.form:
        return jsonify({'error': 'Email required'}), 400
    user_email = request.form['email']
    files = request.files.getlist('images')
    if not files:
        return jsonify({'error': 'No images'}), 400

    order_id = str(uuid.uuid4())
    temp_dir = TEMP_FOLDER
    os.makedirs(temp_dir, exist_ok=True)

    tasks = []
    dst_paths = []
    for file in files:
        if not allowed_file(file.filename):
            continue
        filename = secure_filename(file.filename)
        src_path = os.path.join(temp_dir, f'orig_{order_id}_{filename}')
        file.save(src_path)
        dst_path = os.path.join(temp_dir, f'blur_{order_id}_{filename}')
        tasks.append(process_single_image.s(src_path, dst_path))
        dst_paths.append(dst_path)

    if not tasks:
        return jsonify({'error': 'No valid images'}), 400

    chord_group = group(tasks)
    callback = make_archive_and_send_email.s(dst_paths, user_email, order_id)
    workflow = chord(chord_group)(callback)
    group_id = workflow.parent.id
    return jsonify({'group_id': group_id, 'order_id': order_id})

@api.route('/status/<group_id>', methods=['GET'])
def get_status(group_id):
    result = GroupResult.restore(group_id)
    if not result:
        return jsonify({'error': 'Group not found'}), 404
    total = len(result.results)
    ready = sum(1 for r in result.results if r.ready())
    failed = sum(1 for r in result.results if r.failed())
    status = 'completed' if ready == total else 'in_progress'
    return jsonify({
        'group_id': group_id,
        'total': total,
        'processed': ready,
        'failed': failed,
        'status': status
    })

@api.route('/subscribe', methods=['POST'])
def subscribe_email():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Email required'}), 400
    subscribe(data['email'])
    return jsonify({'message': f'Subscribed {data["email"]}'}), 200

@api.route('/unsubscribe', methods=['POST'])
def unsubscribe_email():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Email required'}), 400
    unsubscribe(data['email'])
    return jsonify({'message': f'Unsubscribed {data["email"]}'}), 200