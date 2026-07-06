from flask import Flask
from flask_cors import CORS
from config import DEBUG, HOST, PORT, MAX_CONTENT_LENGTH
from models import init_db
from routes import api

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
CORS(app)
app.register_blueprint(api)

init_db()


@app.route('/')
def index():
    return {'status': 'Ankit Kushwaha Portfolio API is running'}


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
