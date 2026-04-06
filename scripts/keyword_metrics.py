import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def compute_keyword_scores(df):
    df['word_count'] = df['keyword'].apply(lambda x: len(str(x.split())))
    
    # Competition = how many sources mention this keyword
    # (More sources = more competition)
    df['source_count'] = df.groupby('keyword')['source'].transform('count')
    df['competition'] = df['source_count'] * 100000  # Scale up
    
    df['raw_score'] = (1/df['competition']) * df['word_count']
    
    scaler = MinMaxScaler(feature_range=(0,100))
    df['score'] = scaler.fit_transform(df[["raw_score"]])
    df['score'] = df['score'].round(2)
    df = df.drop(columns=['raw_score'])
    
    return df.sort_values(by='score', ascending=False)