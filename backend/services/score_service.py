from typing import List, Dict
from sqlalchemy import desc, func
from models.score import Score
from models.user import User
from utils.db import db


class ScoreService:

    @staticmethod
    def calculate_score(session, puzzle):
        """
        返回整数分数：
        - success：原规则（0–100）
        - fail（放弃/失败）：倒扣，每交互一次 -10 分（至少 -10）
        """

        # 失败：倒扣（每次交互 -10）
        if getattr(session, "status", None) == "fail":
            used = int(getattr(session, "question_count", 0) or 0)
            return -10 * max(1, used)

        mode = session.mode

        if mode == "free":
            base = 100
            used = session.question_count
            score = max(10, base - used * 5)

        elif mode == "timed":
            total_time = 300
            used_time = (session.end_time - session.start_time).total_seconds()
            remaining = max(0, total_time - used_time)
            score = int(50 + remaining / 6)

        elif mode == "limited_questions":
            total_q = 20
            used = session.question_count
            remaining = max(0, total_q - used)
            score = 40 + remaining * 3

        else:
            score = 0

        return max(0, min(100, score))

    @staticmethod
    def submit_score(user_id: int, puzzle_id: int, score_value: int) -> Score:
        score = Score(user_id=user_id, puzzle_id=puzzle_id, score=score_value)
        db.session.add(score)
        db.session.commit()
        return score

    @staticmethod
    def get_leaderboard(limit: int = 20, lang: str = "zh") -> List[Dict]:
        """
        用户维度排行榜：每个用户的总分（sum(scores.score)）。
        不需要 puzzle 字段。
        """
        rows = (
            db.session.query(
                User.id.label("user_id"),
                User.username.label("username"),
                func.coalesce(func.sum(Score.score), 0).label("total_score"),
            )
            .outerjoin(Score, Score.user_id == User.id)
            .group_by(User.id, User.username)
            .order_by(desc("total_score"), desc("user_id"))
            .limit(limit)
            .all()
        )

        return [
            {"user_id": r.user_id, "username": r.username, "total_score": int(r.total_score)}
            for r in rows
        ]
