from flask import Blueprint, request, jsonify, g
from services.auth_service import AuthService
from utils.jwt import create_token
from utils.auth import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user, error = AuthService.register(username, password)
    if error == "missing_params":
        return jsonify({"error": "missing_params"}), 400
    if error == "user_exists":
        return jsonify({"error": "user_exists"}), 400
    if not user:
        # 理论上不会出现，为类型检查加兜底
        return jsonify({"error": "unknown_error"}), 500

    return jsonify({"message": "registered", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user, error = AuthService.login(username, password)
    if error == "missing_params":
        return jsonify({"error": "missing_params"}), 400
    if error == "invalid_credentials":
        return jsonify({"error": "invalid_credentials"}), 401
    if not user:
        return jsonify({"error": "unknown_error"}), 500

    token = create_token(user.id, user.is_admin)
    return jsonify(
        {
            "message": "login_success",
            "token": token,
            "user": user.to_dict(),
        }
    ), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({"user": g.current_user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    # 前端清理 token，这里仅返回成功占位
    return jsonify({"message": "logout_success"}), 200
