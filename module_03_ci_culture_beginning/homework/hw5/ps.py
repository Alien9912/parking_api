import subprocess
import shlex
from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args = request.args.getlist('arg')
    if not args:
        return "No arguments provided", 400
    safe_args = [shlex.quote(arg) for arg in args]
    command = ['ps'] + safe_args
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return f"<pre>{result.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Error executing ps: {e.stderr}", 500
    except Exception as e:
        return f"Unexpected error: {e}", 500


if __name__ == "__main__":
    app.run(debug=True)