from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def welcome():
    return """
    <html>
        <head>
            <title>arc.dev intro | Sakander Zirai | @suioni</title>
        </head>
        <body>
            <h1>arc.dev Intro Challenge</h1>
            <p>Welcome to the arc dev challange solution of Sakander Zirai <a href="https://arc.dev/@SuiOni">arc.dev/@SuiOni</a> </p> 
            <p>Go to <a href="./docs">docs</a> to see Swagger API Documentation</p>
            <p>Backend is written in Python3 with the FastAPI Framework</p>
            <p>Get the source code from GitHub</p>
        </body>
    </html>
    """
