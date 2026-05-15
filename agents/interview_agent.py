import time
from services.openai_service import chat_completion

from services.score_manager import (
    add_score,
    get_average_score,
    get_full_score_data
)
from services.score_manager import (
    score_answer,
    add_score,
    get_average_score,
    generate_feedback
)

from services.session_memory import (
    interview_state,
    init_interview
)

ASK_PROMPT = "你是一位專業面試官，請根據使用者的問題給出清楚、有幫助的回答。"

FOLLOWUP_PROMPT = """
你是一位真實科技公司的 AI 面試官。

規則：

- 一次只能問一題
- 禁止一次列出多個問題
- 禁止條列式問題
- 問題要像真人面試
- 問題保持簡短
- 根據使用者回答追問
- 不要解釋太多
- 不要輸出 markdown
- 不要輸出編號

請自然輸出下一個追問。

只輸出問題本身。
"""

EVALUATE_PROMPT = """
你是一位資深軟體工程面試官。

請根據使用者回答進行評估。

評估面向：

1. 技術能力
2. 表達能力
3. 實務經驗
4. 問題解決能力
5. 回答完整度

請務必輸出 JSON 格式。

格式如下：

{
    "score": 0-100,
    "strengths": [
        "優點1",
        "優點2"
    ],
    "weaknesses": [
        "缺點1"
    ],
    "suggestions": [
        "建議1"
    ]
}

不要輸出 markdown。
不要輸出 ```json。
只輸出純 JSON。
"""

SCORE_PROMPT = """
你是一位技術面試評分 AI。

請根據使用者回答進行評分。

評分標準：

1. 技術正確性
2. 邏輯性
3. 清晰度
4. 深度

請只輸出 0~100 的整數。

不要解釋。
"""

INTERVIEW_FLOW_PROMPT = """
你是一個 AI 面試流程決策 Agent。

你會根據使用者的回答品質，決定下一步。

規則：

1. 如果回答太簡短或不完整，回傳 FOLLOW_UP
2. 如果回答有內容但需要更深入，回傳 DEEPER_QUESTION
3. 如果回答足夠完整，回傳 NEXT_QUESTION

只能回傳以下其中一個：
FOLLOW_UP
DEEPER_QUESTION
NEXT_QUESTION
"""

DIFFICULTY_PROMPT = """
你是一位資深科技公司 AI 面試官。

請根據使用者回答程度，
判斷他的能力等級。

規則：

- beginner
  幾乎只有基礎概念

- intermediate
  有實作經驗與專案經驗

- advanced
  有系統設計、AI、部署、架構、效能優化等能力

請只輸出：

beginner
intermediate
advanced

不要輸出其他內容。
"""

FOLLOW_UP_RESPONSE_PROMPT = """
你是一位科技公司 AI 技術面試官。

你的風格像：

- Google
- OpenAI
- 新創公司 backend engineer interviewer

規則：

1. 一次只問一個問題
2. 問題保持簡短
3. 不要一次列出多個子問題
4. 保持自然口語
5. 像真人面試官
6. 不要教學
7. 不要解釋
8. 不要給提示
9. 不要輸出 markdown
10. 問題長度不超過兩句

你的目標：

根據使用者剛剛回答不完整的地方追問。

只輸出問題。
"""

DEEPER_QUESTION_RESPONSE_PROMPT = """
你是一位資深 AI 技術面試官。

使用者回答不錯。

請：

- 深入追問技術細節
- 一次只問一題
- 問題像真人技術面試
- 不要條列
- 不要編號
- 保持自然
- 問題簡短有力

只輸出問題。
"""

NEXT_QUESTION_RESPONSE_PROMPT = """
你是一位科技公司 AI 技術面試官。

你的風格像：

- Google
- OpenAI
- AI startup interviewer

規則：

1. 一次只問一個問題
2. 問題簡短自然
3. 不要一次問很多件事
4. 不要解釋
5. 不要教學
6. 不要輸出 markdown
7. 保持像真人面試
8. 問題不要超過兩句

現在請自然切換到下一個技術問題。

題目領域：

- Python
- Backend
- API
- Database
- AI
- Agent
- Software Engineering

只輸出問題。
"""

FINAL_REPORT_PROMPT = """
你是一位資深技術主管。

請根據整場面試紀錄：

1. 分析候選人優勢
2. 分析技術弱點
3. 評估溝通能力
4. 評估技術深度
5. 給出學習建議
6. 判斷是否錄取

請用以下格式：

【整體評價】

【技術優勢】

【技術弱點】

【建議】

【錄取結果】

使用繁體中文。
"""


def ask_question(
    question: str,
    session_id: str
) -> str:

    return chat_completion(
        ASK_PROMPT,
        question,
        session_id
    )

def generate_followup(
    answer: str,
    session_id: str
) -> str:

    return chat_completion(
        FOLLOWUP_PROMPT,
        answer,
        session_id
    )

def evaluate_answer(
    answer: str,
    session_id: str
) -> str:
    
    return chat_completion(
    EVALUATE_PROMPT,
    answer,
    session_id
)

def score_answer(
    answer: str,
    session_id: str
):

    result = chat_completion(
        SCORE_PROMPT,
        answer,
        session_id
    )

    try:
        return int(result.strip())

    except:
        return 60


def decide_interview_flow(
    answer: str,
    session_id: str
) -> str:
    
    return chat_completion(
        INTERVIEW_FLOW_PROMPT,
        answer,
        session_id
    ).strip().upper()

def detect_difficulty(
    answer: str,
    session_id: str
) -> str:

    return chat_completion(
        DIFFICULTY_PROMPT,
        answer,
        session_id
    ).strip().lower()


def generate_interview_response(
    answer: str,
    session_id: str
):
    init_interview(session_id)

    decision = decide_interview_flow(
    answer,
    session_id
    )
    
    difficulty = detect_difficulty(
        answer,
        session_id
    )

    print("decision =", repr(decision))
    
    if decision == "FOLLOW_UP":
        system_prompt = FOLLOW_UP_RESPONSE_PROMPT

    elif decision == "DEEPER_QUESTION":
        system_prompt = DEEPER_QUESTION_RESPONSE_PROMPT

    elif decision == "NEXT_QUESTION":
        system_prompt = NEXT_QUESTION_RESPONSE_PROMPT

    else:
        decision = "FOLLOW_UP"
        system_prompt = FOLLOW_UP_RESPONSE_PROMPT


    current_topic = interview_state[session_id]["current_topic"]

    if current_topic == "python":

        system_prompt += """

    目前主題是 Python。

    請只問：
    - Python syntax
    - data structure
    - OOP
    - async
    - package

    不要跳到其他主題。
    """

    elif current_topic == "fastapi":

        system_prompt += """

    目前主題是 FastAPI。

    請只問：
    - API
    - routing
    - async
    - middleware
    - dependency injection

    不要跳到其他主題。
    """

    interview_state[session_id]["message_count"] += 1

    if decision == "NEXT_QUESTION":
        interview_state[session_id]["main_question_count"] += 1
    else:
        interview_state[session_id]["followup_count"] += 1



    message_count = interview_state[session_id]["message_count"]

    score = score_answer(
        answer,
        session_id
    )

    topic_progress = interview_state[session_id]["topic_progress"]

    current_topic = interview_state[session_id]["current_topic"]

    main_question_count = interview_state[session_id]["main_question_count"]

    elapsed_time = (
        time.time()
        - interview_state[session_id]["start_time"]
    )

    remaining_time = max(
        0,
        interview_state[session_id]["round_duration"]
        - elapsed_time
    )

    if main_question_count >= 3:
        interview_state[session_id]["current_topic"] = "fastapi"

    if main_question_count >= 5:
        interview_state[session_id]["current_topic"] = "database"

    if main_question_count >= 7:
        interview_state[session_id]["current_topic"] = "system_design"

    if remaining_time <= 0:

        interview_state[session_id]["interview_finished"] = True

        final_report = generate_final_report(session_id)

        return {
            "type": "final_report",
            "report": final_report["report"],
            "average_score": get_average_score(session_id),
            "interview_finished": True
        }

    
    result = chat_completion(
        system_prompt,
        answer,
        session_id
    )

    print(type(result))
    print(result)

    add_score(
        session_id,
        score,
        result
    )

    average_score = get_average_score(session_id)

    return {
        "type": "question",
        "decision": decision,
        "difficulty": difficulty,
        "score": score,
        "average_score": average_score,
        "feedback": generate_feedback(score),
        "ai_response": result,
        "main_question_count":
            interview_state[session_id]["main_question_count"],

        "followup_count":
            interview_state[session_id]["followup_count"],
        "message_count": message_count,
        "remaining_time": int(remaining_time),
        "current_topic": interview_state[session_id]["current_topic"],
        "interview_finished":
            interview_state[session_id]["interview_finished"]
    }

def generate_final_report(session_id):

    score_data = get_full_score_data(session_id)

    history = score_data["history"]

    formatted_history = ""

    for index, item in enumerate(history):

        formatted_history += f"""
        第 {index + 1} 題：

        分數：
        {item["score"]}

        AI 回饋：
        {item["feedback"]}
        """



    result = chat_completion(
        FINAL_REPORT_PROMPT,
        formatted_history,
        session_id
    )

    if not result:
        result = "面試報告生成失敗"

    return {
        "average_score": get_average_score(session_id),
        "report": result
    }