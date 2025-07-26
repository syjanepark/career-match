from fastapi import FastAPI
from google import genai
from google.genai import types
from pydantic import BaseModel

class quizAnswers(BaseModel):
    personality: str
    weekend: str
    solving: str
    environtment: str 
    role: str
    motivates: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is working!"}