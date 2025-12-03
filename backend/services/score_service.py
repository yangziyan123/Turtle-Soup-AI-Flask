# backend/services/score_service.py

class ScoreService:

    @staticmethod
    def calculate_score(session, puzzle):
        """
        返回整数分数，根据不同模式使用不同规则
        """

        mode = session.mode

        # ====== 1. 自由模式：提问越少分越高 ======
        if mode == "free":
            base = 100
            used = session.question_count
            score = max(10, base - used * 5)   # 每多问一个扣5分

        # ====== 2. 限时模式：剩余时间越多分越高 ======
        elif mode == "timed":
            total_time = 300   # 5分钟
            used_time = (session.end_time - session.start_time).total_seconds()
            remaining = max(0, total_time - used_time)
            score = int(50 + remaining / 6)   # 最多100分

        # ====== 3. 限题模式：剩余提问越多分越高 ======
        elif mode == "limited_questions":
            total_q = 20
            used = session.question_count
            remaining = max(0, total_q - used)
            score = 40 + remaining * 3

        else:
            score = 0

        return max(0, min(100, score))  # 限制到 0–100 区间
