# backend/services/game_service.py

from models.session import GameSession
from models.score import Score
from utils.db import db
from datetime import datetime
from services.ai_service import AiService
from services.score_service import ScoreService

ALLOWED_MODES = ["free", "timed", "limited_questions"]

class GameService:

    @staticmethod
    def start_game(puzzle_id, user_id, mode):
        # 检查模式是否有效
        if mode not in ALLOWED_MODES:
            return None, "invalid_mode"

        # TODO: 检查 puzzle 是否存在（需要后端A接口）
        # 例如：puzzle = Puzzle.query.get(puzzle_id)
        # 现在先略过
        if not puzzle_id:
            return None, "invalid_puzzle"

        # 创建游戏 session
        session = GameSession(
            puzzle_id=puzzle_id,
            user_id=user_id,
            mode=mode
        )

        db.session.add(session)
        db.session.commit()

        return session, None
    
    @staticmethod
    def chat(session_id, user_question, puzzle):
        """
        puzzle 参数来自 puzzles 表：
        puzzle.description
        puzzle.standard_answer
        """

        session = GameSession.query.get(session_id)
        if not session:
            return None, "session_not_found"

        # —— 限时模式检查 ——
        if session.mode == "timed":
            now = datetime.utcnow()
            diff = (now - session.start_time).total_seconds()
            if diff > 300:
                return None, "time_over"

        # —— 限题模式检查 ——
        if session.mode == "limited_questions":
            if session.question_count >= 20:
                return None, "question_limit_reached"

        # —— 判断是否猜谜底 ——
        if AiService.is_guessing_answer(user_question):
            correct = AiService.check_guess_correct(
                puzzle.standard_answer,
                user_question
            )
            return ("回答正确！你猜到了真相。" if correct else "不对哦，再想想。"), "guess_result"

        # —— 普通 yes/no 回答 ——
        ai_answer = AiService.yes_no_answer(
            puzzle.description,
            user_question
        )

        # —— 更新提问次数 ——
        session.question_count += 1
        db.session.commit()

        return ai_answer, None
    
    @staticmethod
    def finish_game(session_id, result, puzzle):
        """
        result = "success" / "fail"
        """
        session = GameSession.query.get(session_id)
        if not session:
            return None, "session_not_found"

        # 如果已经结束，不允许重复结束
        if session.end_time is not None:
            return None, "already_finished"

        # 1. 设置结束时间和状态
        session.end_time = datetime.utcnow()
        session.status = result
        db.session.commit()

        # 2. 计算得分（失败也可以记录）
        score_value = ScoreService.calculate_score(session, puzzle)

        # 3. 写入 scores 表
        score = Score(
            user_id=session.user_id,
            puzzle_id=session.puzzle_id,
            score=score_value
        )

        db.session.add(score)
        db.session.commit()

        return score_value, None