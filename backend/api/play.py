# backend/api/play.py
from flask import Blueprint, request
from models.session import GameSession
from services.game_service import GameService

# 需要从 puzzles 表获取题目
# 后端A负责 puzzle 模型，这里先做示例
# from models.puzzle import Puzzle   # ⚠ 需要后端A提供
from models.puzzle import get_mock_puzzle


play_bp = Blueprint('play', __name__)

@play_bp.route('/start', methods=['POST'])
def start_game():
    data = request.json or {}

    puzzle_id = data.get("puzzle_id")
    mode = data.get("mode")

    # TODO：从登录态获取真实 user_id
    # 目前先写死为用户 1，后端A提供 login 后替换
    user_id = 1

    # 参数检查
    if not puzzle_id or not mode:
        return {"error": "missing_params"}, 400

    session, error = GameService.start_game(
        puzzle_id=puzzle_id,
        user_id=user_id,
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
        "start_time": session.start_time.isoformat(),
        # 如果是限时模式，前端需要开始计时
        "limit_seconds": 300 if session.mode == "timed" else None,
        # 如果是限制提问模式，前端需要显示剩余次数
        "limit_questions": 20 if session.mode == "limited_questions" else None
    }, 200

@play_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    session_id = data.get("session_id")
    question = data.get("question")

    if not session_id or not question:
        return {"error": "missing_params"}, 400

    # —— 从 puzzles 表获取完整题目（靠后端A） ——
    session = GameSession.query.get(session_id)
    if not session:
        return {"error": "session_not_found"}, 404

    # puzzle = Puzzle.query.get(session.puzzle_id)
    puzzle = get_mock_puzzle(session.puzzle_id)
    if not puzzle:
        return {"error": "puzzle_not_found"}, 404

    # —— 调用服务层逻辑 ——
    reply, error = GameService.chat(
        session_id=session_id,
        user_question=question,
        puzzle=puzzle
    )

    # —— 错误处理 ——
    if error == "session_not_found":
        return {"error": "session_not_found"}, 404

    if error == "time_over":
        return {"error": "time_over"}, 403

    if error == "question_limit_reached":
        return {"error": "question_limit_reached"}, 403

    if error == "guess_result":
        return {"answer": reply, "type": "guess_result"}, 200

    # —— 正常返回 ——
    return {
        "answer": reply,
        "type": "normal"
    }, 200

@play_bp.route('/finish', methods=['POST'])
def finish_game():
    data = request.json or {}
    session_id = data.get("session_id")
    result = data.get("result")   # "success" or "fail"

    if not session_id or not result:
        return {"error": "missing_params"}, 400

    # 找到 session
    session = GameSession.query.get(session_id)
    if not session:
        return {"error": "session_not_found"}, 404

    # 找到对应题目
    # puzzle = Puzzle.query.get(session.puzzle_id)
    puzzle = get_mock_puzzle(session.puzzle_id)
    if not puzzle:
        return {"error": "puzzle_not_found"}, 404

    score_value, error = GameService.finish_game(session_id, result, puzzle)

    # 错误处理
    if error == "session_not_found":
        return {"error": "session_not_found"}, 404
    if error == "already_finished":
        return {"error": "already_finished"}, 400

    # 正常返回
    return {
        "message": "game_finished",
        "result": result,
        "score": score_value
    }, 200
