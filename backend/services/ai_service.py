# backend/services/ai_service.py

class AiService:

    @staticmethod
    def is_guessing_answer(question: str):
        """
        判断玩家是否在猜谜底：
        简单规则：包含“答案”“是不是”“是否”“真相”等词
        """
        guess_keywords = ["是不是", "是否", "答案", "真相", "谜底"]
        return any(k in question for k in guess_keywords)

    @staticmethod
    def check_guess_correct(standard_answer: str, user_question: str):
        """
        判断猜底是否正确：
        简单规则：只要标准答案关键字都出现即视为正确
        """
        key_parts = standard_answer.replace("，", "").replace("。", "").split()
        return all(part in user_question for part in key_parts)

    @staticmethod
    def yes_no_answer(puzzle_description: str, question: str):
        """
        简单版 yes/no AI：
        1. 如果问题包含 puzzle_description 中的关键词 → 答“是”
        2. 否则 → “无关”
        """
        question = question.lower()

        # 简化：根据一些常见关键词做判断
        yes_keywords = ["在", "因为", "关于", "涉及"]
        no_keywords = ["不", "没有"]

        if any(k in question for k in no_keywords):
            return "否"
        if any(k in question for k in yes_keywords):
            return "是"

        return "无关"
