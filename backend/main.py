from fastapi import FastAPI
from google import genai
from google.genai import types
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is working!"}