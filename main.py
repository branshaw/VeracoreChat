from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")

    response = client.chat.completions.create(
        model="gpt-4o",  # or gpt-4-turbo if you want
        messages=[
            {"role": "system", "content": "You are Vera, a thoughtful AI who tracks ideas, tasks, and agents for Bill."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    return {"response": reply}
