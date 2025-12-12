# backend/api/scores.py
from flask import Blueprint

scores_bp = Blueprint('scores', __name__)

@scores_bp.route('', methods=['GET'])
def get_scores():
    """
    获取排行榜：
    未来会支持分页、排序等
    """
    # TODO: 调用 score_service.get_leaderboard()
    dummy_scores = [
        {"username": "alice", "score": 100},
        {"username": "bob", "score": 80},
    ]
    return {
        "message": "scores - TODO",
        "data": dummy_scores
    }, 200
