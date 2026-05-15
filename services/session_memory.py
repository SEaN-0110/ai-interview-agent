import time
from services.redis_service import redis
import json
conversation_memory = None
interview_state = {}

def init_interview(session_id):

    if session_id not in interview_state:
       interview_state[session_id] = {
        "message_count": 0,

        "main_question_count": 0,
        "followup_count": 0,
        
        "current_topic": "python",

        "start_time": time.time(),
        "round_duration": 600,

        "topic_progress": {
            "python": 0,
            "fastapi": 0,
            "database": 0,
            "system_design": 0
        },

        "interview_finished": False
    }
       
def save_conversation(session_id, data):
    redis.set(
        f"conversation:{session_id}",
        json.dumps(data)
    )


def get_conversation(session_id):
    data = redis.get(f"conversation:{session_id}")

    if data:
        return json.loads(data)

    return []

def clear_conversation(session_id):
    redis.delete(f"conversation:{session_id}")


def conversation_exists(session_id):
    return redis.exists(f"conversation:{session_id}")