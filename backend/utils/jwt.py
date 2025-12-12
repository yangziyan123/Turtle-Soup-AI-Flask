"""
JWT 辅助函数：生成与验证 Token
"""
from datetime import datetime, timedelta
import jwt
from flask import current_app


def _get_secret_key():
    # 回退到默认值以避免缺少配置导致崩溃
    return current_app.config.get("SECRET_KEY", "dev-secret-key")


def create_token(user_id: int, is_admin: bool = False, expires_in: int = 86400):
    """
    生成 JWT：
    - user_id: 用户 ID
    - is_admin: 是否管理员
    - expires_in: 过期时间（秒），默认 1 天
    """
    now = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "is_admin": is_admin,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    token = jwt.encode(payload, _get_secret_key(), algorithm="HS256")
    # PyJWT>=2 返回 str，<2 返回 bytes，这里统一转为 str
    return token if isinstance(token, str) else token.decode("utf-8")


def verify_token(token: str):
    """
    校验 Token，返回 payload 或 None
    """
    try:
        return jwt.decode(token, _get_secret_key(), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
