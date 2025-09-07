from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GEMINI_API_KEY = "AIzaSyBU-5UMs2DgexX2MwVionIXjMUJN043e1g"  # Replace with your actual API key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

class SummarizeRequest(BaseModel):
    text: str
    max_tokens: int = 500

@app.post("/summarize-text")
def summarize_text(request: SummarizeRequest):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    payload = {
        "contents": [
            {"parts": [{"text": f"Summarize the following text: {request.text}"}]}
        ],
        "generationConfig": {
            "maxOutputTokens": request.max_tokens
        }
    }

    # Sending the request to the Gemini API for text summarization
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    # Extracting the summary from the response
    summary_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return {"summary": summary_text}
