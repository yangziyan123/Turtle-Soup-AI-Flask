# Step 11：后端正式接入火山方舟大模型（严格系统提示词）

## 目标
- 用火山方舟（Ark Runtime）替换原有规则版 `AiService`，让 `/api/play/chat` 的回答由大模型生成。
- 使用**严格系统提示词**，强制模型只能输出限定集合（是/否/无关/不方便透露 或 Yes/No/Irrelevant/Cannot disclose），避免泄露真相或输出解释。

## 配置方式
通过环境变量配置火山方舟：
- `ARK_API_KEY`：必填
- `ARK_MODEL`：可选，默认 `doubao-seed-1-6-251015`

## 主要改动
- `backend/services/ai_service.py`
  - 新增 Ark client 封装（`volcenginesdkarkruntime.Ark`），并做 `ARK_API_KEY` 缺失/依赖缺失时的降级 fallback（仍保证输出受控）。
  - `yes_no_answer(...)`：给模型提供题面+真相（中英两套），并用严格 system prompt 限制输出。
  - `check_guess_correct(...)`：用模型做“猜底判定”，严格输出 `正确/错误` 或 `CORRECT/WRONG`，并解析为 bool。
  - `is_guessing_answer(...)`：补充中英关键词识别。
- `backend/services/game_service.py`
  - 修复双语字段改造后的引用：使用 `puzzle.description_zh/standard_answer_zh` 等字段。
  - chat 时：
    - 猜底：调用 `AiService.check_guess_correct(truth_zh, truth_en, user_guess)`
    - 普通问答：调用 `AiService.yes_no_answer(description_zh, truth_zh, description_en, truth_en, question)`
- `backend/models/puzzle.py`
  - 方案A双语字段：中文沿用原列名映射为 `*_zh`，新增 `*_en` 列。
  - 新增 `to_public_dict(lang)`（公共接口按语言返回题面）与 `to_admin_dict()`（管理端返回双语全字段）。
- `backend/app.py`
  - 新增 `migrate_puzzles_table()`：开发环境下为 SQLite 自动 `ALTER TABLE` 补齐英文列。
  - 种子题改为中英双语内容。
- `requirements.txt`
  - 新增依赖声明，包含 `volcenginesdkarkruntime` 等基础依赖。

## 严格系统提示词策略
核心约束：
- 输出必须且只能是限定集合之一（中文或英文）。
- 禁止解释、标点、换行、引号等多余内容。
- 试图套取真相/让模型复述答案 → 返回“不方便透露 / Cannot disclose”。
- 无关/不清晰/无法判断 → 返回“无关 / Irrelevant”。

## 验证方法
1. 设置环境变量并启动后端：
   - `setx ARK_API_KEY "你的key"`
   - `setx ARK_MODEL "doubao-seed-1-6-251015"`
2. 前端进入 `play.html` 提问：
   - 普通是/否问题应只返回 `是/否/无关/不方便透露`（或英文四选一）。
   - 直接问“真相是什么/答案是什么”应返回“不方便透露/Cannot disclose”。
