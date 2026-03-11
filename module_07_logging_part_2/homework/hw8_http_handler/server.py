import json
from flask import Flask, request

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logs = []

@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы
    """
    data = dict(request.form)
    logs.append(data)
    print(f"Received log: {data}")
    return "Log received", 200

@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    import pprint
    return '<pre>' + pprint.pformat(logs) + '</pre>'

if __name__ == '__main__':
    # TODO запустить сервер
    app.run(host='0.0.0.0', port=5000, debug=False)