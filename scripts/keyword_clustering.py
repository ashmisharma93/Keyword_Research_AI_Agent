from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_keywords(df, n=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["keyword"])
    
    kmeans = KMeans(n_clusters=n, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)
    
    return df.sort_values("cluster")
