from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()

# Initialize Anthropic client with error handling
try:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    print(f"API key length: {len(api_key)}")
    print(f"API key starts with: {api_key[:10]}...")
    client = anthropic.Anthropic(api_key=api_key)
    print("Anthropic client initialized successfully")
except Exception as e:
    print(f"Error initializing Anthropic client: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
    client = None

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
    # Check if API key is set (without exposing the actual key)
    api_key_set = "ANTHROPIC_API_KEY" in os.environ and os.environ["ANTHROPIC_API_KEY"] != ""
    api_key_length = len(os.environ.get("ANTHROPIC_API_KEY", ""))
    return {
        "message": "Welcome to the Career Coach API! Use /match endpoint to get job recommendations based on quiz answers.",
        "api_key_configured": api_key_set,
        "api_key_length": api_key_length,
        "client_initialized": client is not None
    }

@app.options("/match")
async def options_match():
    return {"message": "OPTIONS request handled"}


@app.post("/match")
async def match(answer: quizAnswers):
    # Check if client is initialized
    if client is None:
        return {"error": "Anthropic client not initialized. Please check your API key."}
    
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
    
    try:
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
        
    except Exception as e:
        return {"error": f"Anthropic API error: {str(e)}"}

    