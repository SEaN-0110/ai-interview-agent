user_scores = {}

def score_answer(answer, session_id):

    score = min(len(answer) * 2, 100)

    return score

def init_score(session_id):

    if session_id not in user_scores:

        user_scores[session_id] = {
            "total_score": 0,
            "questions_count": 0,
            "history": []
        }


def add_score(session_id, score, feedback):

    init_score(session_id)

    user_scores[session_id]["total_score"] += score

    user_scores[session_id]["questions_count"] += 1

    user_scores[session_id]["history"].append({
        "score": score,
        "feedback": feedback
    })


def get_average_score(session_id):

    init_score(session_id)

    total = user_scores[session_id]["total_score"]

    count = user_scores[session_id]["questions_count"]

    if count == 0:
        return 0

    return round(total / count, 2)


def get_score_history(session_id):

    init_score(session_id)

    return user_scores[session_id]["history"]

def get_full_score_data(session_id):

    init_score(session_id)

    return user_scores[session_id]

def generate_feedback(score):

    if score >= 90:
        return "Excellent answer. Strong technical depth."

    elif score >= 75:
        return "Good answer. Could improve clarity and detail."

    elif score >= 60:
        return "Average answer. Need stronger technical explanation."

    else:
        return "Weak answer. Need more practice."