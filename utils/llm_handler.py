import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class LLMHandler:
    """Handles AI-driven insights and question answering using Google Gemini."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=api_key)

    def generate_insights(self, df):
        try:
            sample_data = df.head(5).to_string()
            prompt = (
                "You are a data analyst. Given the following dataset sample:\n"
                f"{sample_data}\n\n"
                "Provide key insights, patterns, and possible trends in simple English."
            )
            model = genai.GenerativeModel('gemini-pro-latest')
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
            else:
                return "No insights generated."
        except Exception as e:
            return f"⚠️ Error generating insights: {str(e)}"

    def answer_question(self, df, question):
        try:
            sample_data = df.head(5).to_string()
            prompt = (
                f"Dataset sample:\n{sample_data}\n\n"
                f"Question: {question}\n"
                "Answer the question using the dataset and explain briefly."
            )
            model = genai.GenerativeModel('gemini-pro-latest')
            response = model.generate_content(prompt)
            if response.text:
                return response.text.strip()
            else:
                return "No answer received from the model."
        except Exception as e:
            return f"⚠️ Error answering question: {str(e)}"
