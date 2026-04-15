import pandas as pd
import numpy as np
import re

def compute_keyword_scores(df):
    # Clean keywords first (remove special characters, extra spaces)
    df['keyword_clean'] = df['keyword'].apply(lambda x: clean_keyword(x))
    
    # Count words on CLEANED keywords
    df['word_count'] = df['keyword_clean'].apply(lambda x: len(str(x).split()))
    
    # Source-based competition 
    df['source_count'] = df.groupby('keyword')['source'].transform('count')
     
    # Factor 1: Competition Score (Lower is better)
    max_sources = df['source_count'].max()
    min_sources = df['source_count'].min()
    
    if max_sources > min_sources:
        df['competition_score'] = 100 * ((max_sources - df['source_count']) / (max_sources - min_sources))
    else:
        df['competition_score'] = 50
    
    # Factor 2: Word Count Score (3-4 words is ideal)
    df['word_count_score'] = df['word_count'].apply(calculate_word_count_score)
    
    # Factor 3: Source Diversity Score
    df['source_diversity'] = df.groupby('keyword')['source'].transform('nunique')
    df['diversity_score'] = (df['source_diversity'] / df['source_diversity'].max()) * 100
    
    # Factor 4: Search Trend Score (keywords from Google/Bing/YouTube = real searches)
    # Gemini-only keywords are AI-generated, so lower priority
    df['trend_score'] = df['source'].apply(lambda x: 100 if x in ['google', 'bing', 'youtube'] else 60)
    
    # Factor 5: Keyword Uniqueness Score
    # Penalize keywords that are too similar to each other (keyword length variance)
    df['keyword_length'] = df['keyword_clean'].apply(lambda x: len(str(x)))
    median_length = df['keyword_length'].median()
    df['uniqueness_score'] = 100 - (abs(df['keyword_length'] - median_length) / df['keyword_length'].max() * 50)
    df['uniqueness_score'] = df['uniqueness_score'].clip(lower=50)  # Min 50
    
    # ============ WEIGHTED COMBINATION ============
    # 40% Competition (find untapped keywords - most important)
    # 25% Word Count (long-tail keywords more valuable)
    # 15% Diversity (multiple sources = validated)
    # 12% Trend (real search data > AI-generated)
    # 8% Uniqueness (bonus for varied keywords)
    
    df['score'] = (
        (df['competition_score'] * 0.40) +
        (df['word_count_score'] * 0.25) +
        (df['diversity_score'] * 0.15) +
        (df['trend_score'] * 0.12) +
        (df['uniqueness_score'] * 0.08)
    )
    
    # Round to 2 decimals
    df['score'] = df['score'].round(2)

    # Clean up temporary columns
    df = df.drop(columns=[
        'source_count', 
        'competition_score', 
        'word_count_score', 
        'diversity_score',
        'source_diversity',
        'trend_score',
        'keyword_length',
        'uniqueness_score',
        'keyword_clean'
    ])
    
    return df.sort_values(by='score', ascending=False)


def calculate_word_count_score(word_count):
    """
    Score based on word count:
    - 1 word: 30 (too generic)
    - 2 words: 70 (decent)
    - 3 words: 100 (optimal long-tail)
    - 4 words: 100 (optimal long-tail)
    - 5 words: 95 (getting too long)
    - 6+ words: 80 (too long)
    """
    if word_count <= 1:
        return 30
    elif word_count == 2:
        return 70
    elif word_count <= 4:
        return 100
    elif word_count == 5:
        return 95
    else:
        return 80


def clean_keyword(keyword):
    """
    Clean keyword by removing special characters and extra spaces
    """
    if pd.isna(keyword):
        return ""
    
    keyword_str = str(keyword).strip()
    
    # Remove markdown-style formatting
    keyword_str = keyword_str.replace('**', '').replace('*', '').replace('_', '')
    
    # Remove common special characters
    keyword_str = re.sub(r'[«»"""\-–—]', ' ', keyword_str)
    
    # Remove bullet points and numbering
    keyword_str = re.sub(r'^[\d\.\)\-\*•]+\s*', '', keyword_str)
    
    # Replace multiple spaces with single space
    keyword_str = re.sub(r'\s+', ' ', keyword_str)
    
    return keyword_str.strip()