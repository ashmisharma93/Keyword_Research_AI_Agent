import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

def enrich_keywords_with_gemini(seed_keyword, n=10):
    prompt = f"Generate {n} long-tail keywords related to '{seed_keyword}' for SEO in bullet points."

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text

        keywords = [line.strip("-• \n") for line in text.split("\n") if line.strip()]
        return keywords

    except Exception as e:
        print("Gemini Error:", e)
        return []
