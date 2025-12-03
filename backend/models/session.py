# backend/models/game_session.py
from utils.db import db
from datetime import datetime
import uuid

class GameSession(db.Model):
    __tablename__ = 'game_sessions'

    id = db.Column(db.String(36), primary_key=True)  # UUID
    puzzle_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    mode = db.Column(db.String(50), nullable=False)

    question_count = db.Column(db.Integer, default=0)   # 用于“有限问题数”模式
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    
    status = db.Column(db.String(20))  # "success" / "fail" / None（未结束）

    def __init__(self, puzzle_id, user_id, mode):
        self.id = str(uuid.uuid4())
        self.puzzle_id = puzzle_id
        self.user_id = user_id
        self.mode = mode
