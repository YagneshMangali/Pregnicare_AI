# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai # type: ignore
# from typing import List, Dict
# import re  # Add this import

# # Load environment variables
# load_dotenv()

# # Configure Google Gemini
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")
# genai.configure(api_key=GOOGLE_API_KEY)

# # Initialize the Gemini model
# model = genai.GenerativeModel('gemini-pro')

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # In-memory chat history
# chat_history: List[Dict[str, str]] = []

# class Query(BaseModel):
#     message: str

# def format_response(text: str) -> str:
#     """Add empathy and motivation to responses."""
#     empathetic_responses = [
#         "You're doing an amazing job, mama! 💖",
#         "I'm here for you. You're not alone. 🤗",
#         "Motherhood is challenging, but you're rocking it! 🌸",
#         "Take a deep breath. You've got this! 💪",
#     ]
#     return f"{text}\n\n{empathetic_responses[len(chat_history) % len(empathetic_responses)]}"

# def is_identity_question(message: str) -> bool:
#     """Check for identity questions using regex."""
#     identity_patterns = [
#         r"who\s+are\s+you",
#         r"what('?s| is) your name",
#         r"tell me about yourself",
#         r"what bot is this",
#         r"who am I talking to",
#         r"are you gemini",
#         r"what is this",
#     ]
#     message_lower = message.lower()
#     return any(re.search(pattern, message_lower) for pattern in identity_patterns)

# def is_motivational_question(message: str) -> bool:
#     """Check for support requests."""
#     motivational_phrases = [
#         "i feel tired", "i'm tired", "i am tired", "exhausted",
#         "i'm stressed", "i am stressed", "stressed out",
#         "i need help", "i need support", "overwhelmed",
#         "i need motivation", "i feel alone", "i'm scared"
#     ]
#     message_lower = message.lower()
#     return any(phrase in message_lower for phrase in motivational_phrases)

# def get_motivational_response() -> str:
#     """Return a tailored motivational message."""
#     motivational_responses = [
#         "You're stronger than you think, mama! 💪 Every challenge makes you wiser.",
#         "It's okay to feel tired. Growing a human is hard work! 🌟",
#         "Reach out to loved ones or a support group. You don’t have to do this alone. 🤗",
#         "You’re a superhero in disguise. Keep going! 🦸‍♀️💛",
#     ]
#     return motivational_responses[len(chat_history) % len(motivational_responses)]


# @app.post("/chat")
# async def chat(query: Query):
#     try:
#         user_message = query.message.strip()

#         if is_identity_question(user_message):
#             bot_response = (
#                 "I am **Pregnicare AI Bot** 🤖💜, your companion for pregnancy and motherhood. "
#                 "Ask me anything about prenatal care, nutrition, or emotional support! 😊"
#             )
#         elif is_motivational_question(user_message):
#             bot_response = get_motivational_response()
#         else:
#             # Debugging: Print the user message to check what is being sent
#             print(f"User Message: {user_message}")
            
#             # Ensure the API call is structured correctly
#             response = model.generate_content(user_message)
            
#             # Debugging: Print the response object to inspect the structure
#             print(f"API Response: {response}")

#             # Check if the response object has `text` attribute
#             if hasattr(response, "text") and response.text:
#                 bot_response = format_response(response.text)
#             elif hasattr(response, "candidates") and response.candidates:
#                 bot_response = format_response(response.candidates[0].content)
#             else:
#                 raise ValueError("No valid response from Gemini API.")

#         # Update chat history
#         chat_history.append({"role": "user", "content": user_message})
#         chat_history.append({"role": "Pregnicare AI Bot", "content": bot_response})

#         return {"response": bot_response}
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Debugging: Print the exact error
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/history")
# async def get_history():
#     return {"history": chat_history}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)









# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai  # type: ignore
# from typing import List, Dict
# import re

# # Load environment variables
# load_dotenv()

# # Configure Google Gemini
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GOOGLE_API_KEY:
#     raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")
# genai.configure(api_key=GOOGLE_API_KEY)

# # Initialize the Gemini model
# model = genai.GenerativeModel('gemini-pro')

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # In-memory chat history
# chat_history: List[Dict[str, str]] = []

# class Query(BaseModel):
#     message: str

# def format_response(text: str) -> str:
#     """Format response using bold headings, bullet points, and proper HTML."""
#     text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  # Convert **bold** to <b>bold</b>
#     text = text.replace("\n", "<br>")  # Line breaks
#     text = re.sub(r"- (.*?)(?=\n|$)", r"<li>\1</li>", text)  # Convert "- " to bullet points
#     text = re.sub(r"(<li>.*?</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)  # Wrap bullet points in <ul>
#     return text

# @app.post("/chat")
# async def chat(query: Query):
#     try:
#         user_message = query.message.strip()

#         if user_message.lower() in ["hi", "hello", "hey"]:
#             bot_response = "<b>Hello, Mama! 🤗</b><br>How can I assist you today?"
#         elif "who are you" in user_message.lower():
#             bot_response = "<b>I am Pregnicare AI Bot 🤖💜</b><br>Your companion for pregnancy and motherhood! Ask me anything about prenatal care, nutrition, or emotional well-being. 😊"
#         else:
#             # Generate response using Gemini API
#             response = model.generate_content(user_message)

#             # Extract response text correctly
#             if hasattr(response, "text") and response.text:
#                 bot_response = format_response(response.text)
#             elif hasattr(response, "candidates") and response.candidates:
#                 bot_response = format_response(response.candidates[0].content)
#             else:
#                 raise ValueError("No valid response from Gemini API.")

#         # Append chat history
#         chat_history.append({"role": "user", "content": user_message})
#         chat_history.append({"role": "Pregnicare AI Bot", "content": bot_response})

#         return {"response": bot_response}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/history")
# async def get_history():
#     return {"history": chat_history}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


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








