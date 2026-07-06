from flask import Flask, send_from_directory, abort
from flask_cors import CORS
import os
from config import MAX_CONTENT_LENGTH
from models import init_db
from routes import api

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
CORS(app)
app.register_blueprint(api)

init_db()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path.startswith('api/'):
        abort(404)

    if path in ('', 'index.html'):
        return send_from_directory(ROOT_DIR, 'index.html')

    file_path = os.path.join(ROOT_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(ROOT_DIR, path)

    html_path = path if path.endswith('.html') else f'{path}.html'
    html_file = os.path.join(ROOT_DIR, html_path)
    if os.path.isfile(html_file):
        return send_from_directory(ROOT_DIR, html_path)

    abort(404)


if __name__ == '__main__':
    from config import DEBUG, HOST, PORT
    app.run(debug=DEBUG, host=HOST, port=PORT)
