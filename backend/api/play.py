# backend/api/play.py
from flask import Blueprint, request, g, jsonify
from models.session import GameSession
from models.puzzle import Puzzle
from services.game_service import GameService
from utils.auth import login_required


play_bp = Blueprint('play', __name__)


@play_bp.route('/start', methods=['POST'])
@login_required
def start_game():
    data = request.json or {}

    puzzle_id = data.get("puzzle_id")
    mode = data.get("mode")

    # 参数检查
    if not puzzle_id or not mode:
        return {"error": "missing_params"}, 400

    session, error = GameService.start_game(
        puzzle_id=puzzle_id,
        user_id=g.current_user.id,
        mode=mode
    )

    if error == "invalid_mode":
        return {"error": "invalid_mode"}, 400
    if error == "invalid_puzzle":
        return {"error": "invalid_puzzle"}, 400

    # 成功
    return {
        "message": "game_started",
        "session_id": session.id,
        "mode": session.mode,
        "puzzle_id": session.puzzle_id,
        "start_time": session.start_time.isoformat() + "Z",
        # 如果是限时模式，前端需要开始计时
        "limit_seconds": 300 if session.mode == "timed" else None,
        # 如果是限题提醒，前端需要展示剩余次数
        "limit_questions": 20 if session.mode == "limited_questions" else None
    }, 200


@play_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.json or {}
    session_id = data.get("session_id")
    question = data.get("question")

    if not session_id or not question:
        return {"error": "missing_params"}, 400

    session = GameSession.query.get(session_id)
    if not session:
        return {"error": "session_not_found"}, 404

    # 确保会话归属当前用户
    if session.user_id != g.current_user.id:
        return jsonify({"error": "forbidden"}), 403

    puzzle = Puzzle.query.get(session.puzzle_id)
    if not puzzle:
        return {"error": "puzzle_not_found"}, 404

    reply, error = GameService.chat(
        session_id=session_id,
        user_question=question,
        puzzle=puzzle
    )

    if error == "session_not_found":
        return {"error": "session_not_found"}, 404
    if error == "time_over":
        return {"error": "time_over"}, 403
    if error == "question_limit_reached":
        return {"error": "question_limit_reached"}, 403
    if error == "guess_result":
        return {"answer": reply, "type": "guess_result"}, 200

    return {
        "answer": reply,
        "type": "normal"
    }, 200


@play_bp.route('/finish', methods=['POST'])
@login_required
def finish_game():
    data = request.json or {}
    session_id = data.get("session_id")
    result = data.get("result")   # "success" or "fail"

    if not session_id or not result:
        return {"error": "missing_params"}, 400

    session = GameSession.query.get(session_id)
    if not session:
        return {"error": "session_not_found"}, 404

    # 确保会话归属当前用户
    if session.user_id != g.current_user.id:
        return jsonify({"error": "forbidden"}), 403

    puzzle = Puzzle.query.get(session.puzzle_id)
    if not puzzle:
        return {"error": "puzzle_not_found"}, 404

    score_value, error = GameService.finish_game(session_id, result, puzzle)

    if error == "session_not_found":
        return {"error": "session_not_found"}, 404
    if error == "already_finished":
        return {"error": "already_finished"}, 400

    return {
        "message": "game_finished",
        "result": result,
        "score": score_value
    }, 200
