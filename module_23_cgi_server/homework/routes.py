import json
import re

class WSGIApp:
    def __init__(self):
        self.routes = {}
        self.dynamic = []

    def route(self, path):
        def decorator(func):
            if '<' in path and '>' in path:
                regex = re.sub(r'<([^>]+)>', r'([^/]+)', path)
                self.dynamic.append((re.compile(f'^{regex}$'), func))
            else:
                self.routes[path] = func
            return func
        return decorator

    def _find(self, path):
        if path in self.routes:
            return self.routes[path], []
        for regex, func in self.dynamic:
            m = regex.match(path)
            if m:
                return func, m.groups()
        return None, None

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        if '?' in path:
            path = path.split('?')[0]

        handler, args = self._find(path)
        if handler is None:
            start_response('404 Not Found', [('Content-Type', 'application/json')])
            return [json.dumps({'error': 'Not found'}).encode()]

        result = handler(*args)
        if not isinstance(result, dict):
            result = {'response': str(result)}
        body = json.dumps(result)
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [body.encode()]

app = WSGIApp()

@app.route('/hello')
def hello():
    return {'response': 'Hello, world!'}

@app.route('/hello/<name>')
def hello_name(name):
    return {'response': f'Hello, {name}!'}