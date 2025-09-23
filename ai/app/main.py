import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# In-memory session storage
user_sessions = {}

@app.post("/chat")
async def chat(request: ChatRequest):
    user_id = request.user_id
    user_message = request.message

    # Initialize session if new user
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    # Append user message
    user_sessions[user_id].append({"role": "user", "parts": [user_message]})

    # Call Gemini with full history
    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro
    response = model.generate_content(user_sessions[user_id])

    # Append model response
    bot_reply = response.text
    user_sessions[user_id].append({"role": "model", "parts": [bot_reply]})

    return {"response": bot_reply}
