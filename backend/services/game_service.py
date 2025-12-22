# backend/services/game_service.py

from datetime import datetime
from models.session import GameSession
from models.score import Score
from models.puzzle import Puzzle
from utils.db import db
from services.ai_service import AiService
from services.score_service import ScoreService

ALLOWED_MODES = ["free", "timed", "limited_questions"]


class GameService:

    @staticmethod
    def start_game(puzzle_id, user_id, mode):
        if mode not in ALLOWED_MODES:
            return None, "invalid_mode"

        puzzle = Puzzle.query.get(puzzle_id)
        if not puzzle:
            return None, "invalid_puzzle"

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
        puzzle 来自 puzzles 表（双语字段）：
        - puzzle.description_zh / puzzle.standard_answer_zh
        - puzzle.description_en / puzzle.standard_answer_en
        """
        session = GameSession.query.get(session_id)
        if not session:
            return None, "session_not_found"

        if session.end_time is not None:
            return None, "already_finished"

        if session.mode == "timed":
            now = datetime.utcnow()
            diff = (now - session.start_time).total_seconds()
            if diff > 300:
                return None, "time_over"

        if session.mode == "limited_questions":
            if session.question_count >= 20:
                return None, "question_limit_reached"

        # 玩家可能在任意一句话里表达出已经猜到真相：每次都做一次“是否完全猜出真相”判定
        solved = AiService.check_solved(
            truth_zh=puzzle.standard_answer_zh,
            truth_en=puzzle.standard_answer_en,
            user_text=user_question,
        )
        if solved:
            # 自动结算为成功
            score_value, error = GameService.finish_game(session_id, "success", puzzle)
            if error == "already_finished":
                return None, "already_finished"

            if AiService.detect_language(user_question) == "en":
                msg = "You solved it! Score has been settled."
            else:
                msg = "你已经猜到真相了！已自动结算得分。"

            return {
                "type": "game_over",
                "result": "success",
                "score": score_value,
                "answer": msg,
            }, None

        ai_answer = AiService.yes_no_answer(
            description_zh=puzzle.description_zh,
            truth_zh=puzzle.standard_answer_zh,
            description_en=puzzle.description_en,
            truth_en=puzzle.standard_answer_en,
            question=user_question,
        )

        session.question_count += 1
        db.session.commit()

        return ai_answer, None

    @staticmethod
    def finish_game(session_id, result, puzzle):
        session = GameSession.query.get(session_id)
        if not session:
            return None, "session_not_found"

        if session.end_time is not None:
            return None, "already_finished"

        session.end_time = datetime.utcnow()
        session.status = result
        db.session.commit()

        score_value = ScoreService.calculate_score(session, puzzle)

        score = Score(
            user_id=session.user_id,
            puzzle_id=session.puzzle_id,
            score=score_value
        )

        db.session.add(score)
        db.session.commit()

        return score_value, None
