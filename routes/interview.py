import uuid
from fastapi import APIRouter, Depends
from services.auth import verify_api_key
from fastapi.responses import JSONResponse
from services.session_memory import (
    conversation_memory,
    interview_state,
    init_interview
)

from agents.interview_agent import (
    ask_question,
    decide_interview_flow,
    evaluate_answer,
    generate_followup,
    generate_interview_response,
    generate_final_report
)

router = APIRouter()

def success_response(data=None, message="success"):
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )


def error_response(message="error", status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )

@router.post(
    "/start",
    dependencies=[Depends(verify_api_key)]
)
async def start_interview():

    session_id = str(uuid.uuid4())

    first_question = "請先簡單介紹一下你自己，以及你熟悉的技術。"

    init_interview(session_id)

    conversation_memory[session_id] = [
    {
        "role": "assistant",
        "content": first_question
    }
    ]

    return success_response({
        "type": "start",
        "session_id": session_id,
        "question": first_question
    })


@router.get("/ask")
def ask_ai(
    question: str,
    session_id: str
):
    answer = ask_question(
        question,
        session_id
    )

    return {
        "question": question,
        "answer": answer,
    }


@router.get("/followup")
def followup(
    answer: str,
    session_id: str
):
    result = generate_followup(
        answer,
        session_id
    )

    return {
        "user_answer": answer,
        "ai_followup": result,
    }


@router.get("/evaluate")
def evaluate(
    answer: str,
    session_id: str
):
    result = evaluate_answer(
        answer,
        session_id
    )

    return {
        "evaluation": result
    }

@router.get("/interview_flow")
def interview_flow(
    answer: str,
    session_id: str
):
    decision = decide_interview_flow(
        answer,
        session_id
    )

    return {
        "decision": decision,
    }


from pydantic import BaseModel

class InterviewRequest(BaseModel):
    answer: str
    session_id: str


@router.post(
    "/answer",
    dependencies=[Depends(verify_api_key)]
)
def interview(data: InterviewRequest):

    try:

        response = generate_interview_response(
            data.answer,
            data.session_id
        )

        print(response)

        if response["interview_finished"]:

            interview_state[data.session_id]["final_report"] = response["report"]

            interview_state[data.session_id]["average_score"] = response["average_score"]

            return success_response({
                "type": "final_report",
                "finished": True,
                "report": response["report"],
                "average_score": response["average_score"]
            })

        return success_response({
            "type": "question",

            "interview_finished": False,

            "ai_response": response["ai_response"],

            "decision": response["decision"],
            "difficulty": response["difficulty"],

            "score": response["score"],
            "average_score": response["average_score"],
            "feedback": response["feedback"],

            "main_question_count":
                response["main_question_count"],

            "followup_count":
                response["followup_count"],

            "message_count":
                response["message_count"],

            "remaining_time":
                response["remaining_time"],

            "current_topic":
                response["current_topic"]
        })

    except Exception as e:

        return error_response(str(e), 500)
    
@router.get(
    "/report/{session_id}",
    dependencies=[Depends(verify_api_key)]
)
async def get_report(session_id: str):

    session = interview_state.get(session_id)

    if not session:
        return error_response("Session not found", 404)

    return success_response({
        "type": "report",
        "average_score": session.get("average_score", 0),
        "report": session.get("final_report", "尚未生成報告")
    })

