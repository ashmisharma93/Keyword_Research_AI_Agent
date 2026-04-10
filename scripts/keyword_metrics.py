import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def compute_keyword_scores(df):
    df['word_count'] = df['keyword'].apply(lambda x: len(str(x.split())))

    # Source-based competition 
    df['source_count'] = df.groupby('keyword')['source'].transform('count')
    df['competition'] = df['source_count'] * 20  # Each source = 20 points
    
    # Higher word count + lower competition = higher score
    df['raw_score'] = (df['word_count'] * 100) / (df['competition'] + 1)
    
    # Scale to 0-100 range
    scaler = MinMaxScaler(feature_range=(0, 100))
    df['score'] = scaler.fit_transform(df[["raw_score"]])
    
    # Round to 2 decimals
    df['score'] = df['score'].round(2)

    df = df.drop(columns=['raw_score', 'source_count'])
    
    return df.sort_values(by='score', ascending=False)