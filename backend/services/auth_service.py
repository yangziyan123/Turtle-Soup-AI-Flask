from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.db import db


class AuthService:
    """
    用户注册 / 登录 服务层
    """

    @staticmethod
    def register(username: str, password: str):
        if not username or not password:
            return None, "missing_params"

        exists = User.query.filter_by(username=username).first()
        if exists:
            return None, "user_exists"

        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            is_admin=False,
        )
        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def login(username: str, password: str):
        if not username or not password:
            return None, "missing_params"

        user = User.query.filter_by(username=username).first()
        if not user:
            return None, "invalid_credentials"

        if not check_password_hash(user.password_hash, password):
            return None, "invalid_credentials"

        return user, None

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.query.get(user_id)
