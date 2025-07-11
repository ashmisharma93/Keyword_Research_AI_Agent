import os
import pandas as pd

def save_df(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Saved to {path}")

def print_top(df, n=10):
    print("\n🔝 Top", n, "keywords:")
    print(df.head(n))
