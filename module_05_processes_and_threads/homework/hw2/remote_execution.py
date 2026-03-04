"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

from flask import Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import subprocess
import shutil
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


class CodeForm(FlaskForm):
    code = StringField('code', validators=[DataRequired()])
    timeout = IntegerField('timeout', validators=[DataRequired(), NumberRange(min=1, max=30)])


def run_python_code_in_subprocess(code: str, timeout: int):
    if shutil.which('prlimit'):
        cmd = ['prlimit', '--nproc=1:1', 'python', '-c', code]
    else:
        cmd = [sys.executable, '-c', code]

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate(timeout=timeout)
        if proc.returncode != 0:
            return stderr or f"Process exited with code {proc.returncode}"
        return stdout or stderr
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        return "Timeout exceeded. Process terminated."
    except Exception as e:
        return str(e)


@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()
    if form.validate_on_submit():
        result = run_python_code_in_subprocess(form.code.data, form.timeout.data)
        return jsonify({'result': result})
    else:
        return jsonify({'errors': form.errors}), 400


if __name__ == '__main__':
    app.run(debug=True)