# import numpy as np

# def compute_keyword_scores(df):
#     df["word_count"] = df["keyword"].apply(lambda x: len(str(x).split()))
#     df["competition"] = np.random.randint(10000, 1000000, size=len(df))
#     df["score"] = (1 / df["competition"]) * df["word_count"]
#     return df.sort_values(by="score", ascending=False)

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def compute_keyword_scores(df):
    df['word_count'] = df['keyword'].apply(lambda x: len(str(x.split())))

    df['competition'] = np.random.randint(10000, 1000000, size = len(df))

    df['raw_score'] = (1/df['competition']) * df['word_count']
    
    scaler = MinMaxScaler(feature_range=(0,100))
    df['score'] = scaler.fit_transform(df[["raw_score"]])

    df['score'] = df['score'].round(2)

    df = df.drop(columns=['raw_score'])
    
    return df.sort_values(by='score', ascending = False)