import time
conversation_memory = {}
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