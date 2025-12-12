from functools import wraps
from flask import request, jsonify, g
from models.user import User
from utils.jwt import verify_token


def _get_bearer_token():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def login_required(f):
    """
    校验 Bearer Token，解析后注入 g.current_user
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = _get_bearer_token()
        if not token:
            return jsonify({"error": "unauthorized"}), 401

        payload = verify_token(token)
        if not payload or "user_id" not in payload:
            return jsonify({"error": "unauthorized"}), 401

        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "unauthorized"}), 401

        # 注入当前用户，避免直接挂载到 request 产生类型提示问题
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    先验证登录，再检查管理员权限
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = _get_bearer_token()
        if not token:
            return jsonify({"error": "unauthorized"}), 401

        payload = verify_token(token)
        if not payload or "user_id" not in payload:
            return jsonify({"error": "unauthorized"}), 401

        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "unauthorized"}), 401

        if not user.is_admin:
            return jsonify({"error": "forbidden"}), 403

        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function

