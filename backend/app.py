# backend/app.py
from flask import Flask
from api.play import play_bp
from api.scores import scores_bp
from api.auth import auth_bp
from utils.db import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haiguitang.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(play_bp, url_prefix='/api/play')
    app.register_blueprint(scores_bp, url_prefix='/api/scores')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    @app.route('/ping')
    def ping():
        return {'message': 'pong'}

    return app


if __name__ == '__main__':
    app = create_app()

    # 创建所有表结构
    with app.app_context():
        db.create_all()

    app.run(debug=True)
