import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

def enrich_keywords_with_gemini(seed_keyword, n=10):
    # Improved prompt for cleaner output
    prompt = f"""Generate exactly {n} long-tail keywords related to '{seed_keyword}' for SEO.

Requirements:
- Each keyword should be 2-4 words long
- Return ONLY keywords, one per line
- No numbering, no bullet points, no explanations
- No sentences or phrases, just keywords
- Keywords should be unique and relevant

Example format:
global internship opportunities
summer internship abroad
internship for students

Now generate {n} keywords for '{seed_keyword}':"""

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text

        # Clean up the keywords better
        keywords = [
            line.strip().strip("-• *").strip() 
            for line in text.split("\n") 
            if line.strip() and not line.strip().startswith("Example") and len(line.split()) <= 10
        ]
        
        # Filter out empty lines and very long lines
        keywords = [kw for kw in keywords if kw and len(kw) > 5]
        
        print(f"✓ Gemini enrichment successful! Generated {len(keywords)} clean keywords")
        return keywords

    except Exception as e:
        print("Gemini Error:", e)
        return []