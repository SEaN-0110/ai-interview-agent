from fastapi import FastAPI

from routes.health import router as health_router
from routes.interview import router as interview_router
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from services.score_manager import get_full_score_data

templates = Jinja2Templates(directory="templates")


app = FastAPI()

app.include_router(health_router)
app.include_router(interview_router)

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="chat.html"
    )

@app.get("/report", response_class=HTMLResponse)
def report_page(request: Request):

    data = get_full_score_data("user1")

    history_html = ""

    for item in data["history"]:

        history_html += f"""
        <div style='
            background:white;
            padding:15px;
            margin-bottom:10px;
            border-radius:10px;
        '>

            <b>Score:</b> {item["score"]}<br>
            <b>Feedback:</b> {item["feedback"]}

        </div>
        """

    average = 0

    if data["questions_count"] > 0:
        average = round(
            data["total_score"] / data["questions_count"],
            2
        )

    return f"""

    <html>

    <head>

        <title>Interview Report</title>

    </head>

    <body style="
        font-family:Arial;
        background:#f5f5f5;
        padding:30px;
    ">

        <h1>AI Interview Report</h1>

        <div style="
            background:white;
            padding:20px;
            border-radius:10px;
            margin-bottom:20px;
        ">

            <h2>Summary</h2>

            <p><b>Total Questions:</b> {data["questions_count"]}</p>

            <p><b>Average Score:</b> {average}</p>

        </div>

        <h2>History</h2>

        {history_html}

    </body>

    </html>

    """