import numpy as np

def compute_keyword_scores(df):
    df["word_count"] = df["keyword"].apply(lambda x: len(str(x).split()))
    df["competition"] = np.random.randint(10000, 1000000, size=len(df))
    df["score"] = (1 / df["competition"]) * df["word_count"]
    return df.sort_values(by="score", ascending=False)
