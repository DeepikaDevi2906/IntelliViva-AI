from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, bcrypt, jwt
from routes.auth_routes import auth_bp
from routes.audio_routes import audio_bp
from routes.evaluation_routes import evaluation_bp
from routes.question_routes import question_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(audio_bp, url_prefix="/api/audio")
    app.register_blueprint(evaluation_bp, url_prefix="/api/eval")
    app.register_blueprint(question_bp, url_prefix="/api/question")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)