from fastapi import FastAPI
from model import generate_reply


app = FastAPI()


@app.post("/reply")
def reply(data: dict):
return {"reply": generate_reply(data["text"])}
