from flask import Flask
from flask_cors import CORS
from user_service.feedback import feedback_bp

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(feedback_bp, url_prefix='/api')
@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)