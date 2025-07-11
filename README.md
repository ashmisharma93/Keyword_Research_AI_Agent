# Keyword Research AI Agent with n8n & Gemini

This project is a fully automated AI agent that performs smart keyword research using:

- Python for data collection, enrichment, and scoring
- Gemini API for long-tail keyword expansion
- n8n for no-code workflow automation
- Google Sheets for clean and accessible output

---

## What It Does

This AI-powered agent takes a **seed keyword** (e.g., “Global Internship”) and:

1. 📥 Gathers keyword suggestions from:
   - Google Autocomplete
   - Bing Suggestions
   - YouTube Suggestions
2. Expands with Gemini API to generate semantically rich long-tail keywords
3. Scores each keyword based on:
   ```python
   score = (1 / competition) * word_count
   ```
4. Clusters keywords into topics
5. Saves all results to a Google Sheet
6. Sends a daily email with:
   - Top 10 keywords
   - Google Sheet Link

# 📁 Folder Structure
```
Keyword_Research_AI_Agent/
├── data/
│   ├── raw/                ← Suggestions from Google/Bing/YouTube
│   ├── enriched/           ← Gemini enriched keywords
│   └── processed/          ← Scored & clustered output
├── scripts/
│   ├── main.py
│   ├── keyword_sources.py
│   ├── gpt_enrichment.py
│   ├── keyword_metrics.py
│   ├── keyword_clustering.py
│   └── my_utils.py
├── n8n/
│   ├── screenshots/        ← Workflow images
│   └── upload_keywords_to_sheets.n8n.json
├── .env.example            ← Dummy credentials (safe to share)
├── .gitignore              ← Prevents leaking secrets, .venv, etc.
└── README.md               ← You're here!

```

# Tools Used
Python            - keyword extraction,scoring,clustering
Gemini API        - Long tail-keyword generation
Google Sheets API - Upload final results
n8n               - Workflow automation(daily run + email)
Gmail SMTP        - Daily keyword summary email