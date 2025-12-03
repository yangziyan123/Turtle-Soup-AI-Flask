# backend/models/puzzle.py
# 注意：这是临时的 mock 模型，后端A实现后可删除或替换

class Puzzle:
    def __init__(self, id, description, standard_answer):
        self.id = id
        self.description = description
        self.standard_answer = standard_answer

# 提供一个假题目
MOCK_PUZZLES = {
    1: Puzzle(
        id=1,
        description="一个男人死在房间里，房间里有一滩水。",
        standard_answer="他站在融化的冰块上被吊死"
    )
}

def get_mock_puzzle(puzzle_id):
    return MOCK_PUZZLES.get(puzzle_id)
