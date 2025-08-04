from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:5500",
        "https://career-match-1.onrender.com",
        "https://career-match-0pw6.onrender.com",
        "https://career-match-rho.vercel.app",  # Your specific Vercel domain
        "https://*.vercel.app",  # Allow all Vercel domains
        "*"  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class quizAnswers(BaseModel):
    personality: str
    weekend: str
    solving: str
    environment: str 
    role: str
    motivates: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Career Coach API! Use /match endpoint to get job recommendations based on quiz answers."}

@app.options("/match")
async def options_match():
    return {"message": "OPTIONS request handled"}


@app.post("/match")
async def match(answer: quizAnswers):
    # This function will match the user's answers to a job
    answers = answer.dict()
    personality = answers.get("personality")
    weekend = answers.get("weekend")
    solving = answers.get("solving")
    environment = answers.get("environment")
    role = answers.get("role")
    motivates = answers.get("motivates")

    prompt = f"""
    You are a helpful and fun career coach. Based on the user's answers to the quiz, suggest a suitable job role. The answers are as follows:
    - Personality: {personality}
    - Weekend activity preference: {weekend}
    - Problem-solving approach: {solving}
    - Preferred work environment: {environment}
    - Desired role: {role}
    - Motivating factors: {motivates}

    Provide a job recommendation that aligns with these traits and preferences. Include a brief explanation for the recommendation.
    Format your answer as follows:
       {{
        "job_matches": ["Job 1", "Job 2"],
        "personality_label": "fun and engaging personality label with a fun emoji",
        "strengths": ["Strength 1", "Strength 2", "Strength 3"],
        "growth_area": "One growth suggestion",
        "explanation": "A brief explanation of why this job is a good fit.",
    }}
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # extract the response content
    response_content = response.content[0].text
    # extract the inner JSON string
    match = re.search(r'\{.*\}', response_content, re.DOTALL)
    if not match:
        return {"error": "Failed to extract JSON from the AI model response."}
    response_content = match.group(0)
    # Parsing the response content to a dictionary
    try:
        response_dict = json.loads(response_content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse the response from the AI model."} 
        
    # Return the response dictionary
    return response_dict

    