import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_answer(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"Error generating answer from Gemini: {e}"

def generate_answer_with_image(prompt_parts):
    try:
        response = model.generate_content(prompt_parts)
        return response.text, None
    except Exception as e:
        return None, f"Error generating answer from Gemini with image: {e}"