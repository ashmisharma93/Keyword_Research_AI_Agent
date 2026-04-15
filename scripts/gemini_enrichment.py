import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

def enrich_keywords_with_gemini(seed_keyword, n=20):
    # Improved prompt for cleaner output
    prompt = f"""Generate exactly {n} long-tail keywords related to '{seed_keyword}' for SEO.

STRICT Requirements:
- Each keyword MUST be 2-4 words ONLY
- Return ONLY keywords, one per line
- NO numbering, NO bullet points, NO dashes, NO asterisks
- NO markdown formatting, NO special characters
- NO explanations or descriptions
- NO example text in output
- Just plain text keywords, nothing else
- Each line must be a single keyword

Generate {n} keywords for '{seed_keyword}':"""

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text

        # Parse and clean keywords
        keywords = []
        for line in text.split("\n"):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Remove numbering and bullets
            line = re.sub(r'^[\d\.\)\-\*•\s]+', '', line).strip()
            
            # Remove markdown formatting
            line = re.sub(r'[\*_`~]', '', line)
            
            # Remove special characters
            line = re.sub(r'[«»"""\[\]\{\}]', '', line)
            
            # Skip if it's an example or instruction
            if any(skip in line.lower() for skip in ['example', 'generate', 'keywords', 'requirements', 'output']):
                continue
            
            # Skip very long keywords (should be 2-4 words)
            word_count = len(line.split())
            if word_count < 2 or word_count > 10:  # Allow up to 10 to catch some multi-word phrases
                continue
            
            # Only add if keyword is at least 5 characters
            if len(line) >= 5 and line not in keywords:
                keywords.append(line)
        
        print(f"✓ Gemini enrichment successful! Generated {len(keywords)} clean keywords")
        return keywords[:n]  # Return exactly n keywords

    except Exception as e:
        print("Gemini Error:", e)
        return []