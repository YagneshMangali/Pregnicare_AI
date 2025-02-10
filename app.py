from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai  # type: ignore
from typing import List, Dict
import re

# Load environment variables
load_dotenv()

# Configure Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory chat history
chat_history: List[Dict[str, str]] = []

class Query(BaseModel):
    message: str

def format_response(text: str) -> str:
    """Format response using bold headings, bullet points, and proper HTML."""
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  # Convert **bold** to <b>bold</b>
    text = text.replace("\n", "<br>")  # Line breaks
    text = re.sub(r"- (.*?)(?=\n|$)", r"<li>\1</li>", text)  # Convert "- " to bullet points
    text = re.sub(r"(<li>.*?</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)  # Wrap bullet points in <ul>
    return text

def generate_response(user_message: str) -> str:
    """Generate chatbot response based on user input and chat history."""
    try:
        # Predefined responses for common queries
        predefined_responses = {
            "hi": "<b>Hello, Mama! 🤗</b><br>How can I assist you today?",
            "hello": "<b>Hello, Mama! 🤗</b><br>How can I assist you today?",
            "hey": "<b>Hello, Mama! 🤗</b><br>How can I assist you today?",
            "who are you": "<b>I am Pregnicare AI Bot 🤖💜</b><br>Your companion for pregnancy and motherhood! Ask me anything about prenatal care, nutrition, or emotional well-being. 😊"
        }

        # Return predefined response if available
        normalized_message = user_message.lower().strip()
        if normalized_message in predefined_responses:
            return predefined_responses[normalized_message]

        # Include last 5 messages from chat history for context
        context_messages = chat_history[-5:]  

        # Format conversation history to send to Gemini
        formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context_messages])

        # Build complete prompt with history
        full_prompt = f"Previous conversation:\n{formatted_history}\n\nUser: {user_message}\n\nBot:"

        # Generate response using Gemini API
        response = model.generate_content(full_prompt)

        # Extract response text correctly
        if hasattr(response, "text") and response.text:
            return format_response(response.text)
        elif hasattr(response, "candidates") and response.candidates:
            return format_response(response.candidates[0].content)
        else:
            return "<b>I'm sorry, I couldn't understand that.</b><br>Can you please ask in a different way? 😊"

    except Exception as e:
        return f"<b>Oops! Something went wrong.</b><br>Error: {str(e)}"

@app.post("/chat")
async def chat(query: Query):
    try:
        user_message = query.message.strip()

        # Get response
        bot_response = generate_response(user_message)

        # Append chat history
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "Pregnicare AI Bot", "content": bot_response})

        return {"response": bot_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    return {"history": chat_history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)








