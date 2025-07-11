from keyword_sources import get_google_suggestions, get_bing_suggestions, get_youtube_suggestions
from gemini_enrichment import enrich_keywords_with_gemini
import keyword_metrics
import keyword_clustering
import my_utils
import pandas as pd

print("Functions available in my_utils:", dir(my_utils))
print("keyword_metrics has:", dir(keyword_metrics))


seed = "Global internship"

def to_df(keywords, source):
    return pd.DataFrame({
        "keyword": keywords,
        "source": source,
        "seed": seed
    })

# Fetch suggestions
google = to_df(get_google_suggestions(seed),"google")
bing = to_df(get_bing_suggestions(seed), "bing")
youtube = to_df(get_youtube_suggestions(seed), "youtube")

df_suggest = pd.concat([google,bing,youtube]).drop_duplicates()
my_utils.save_df(df_suggest, "data/raw/all_keywords_suggestion.csv")

# Gemini Enrichment
gemini_keywords = enrich_keywords_with_gemini(seed, n=10)
df_gemini = to_df(gemini_keywords, "gemini")
my_utils.save_df(df_gemini, "data/enriched/enriched_gemini_keywords.csv")

# Combine and Score
df_all = pd.concat([df_suggest, df_gemini]).drop_duplicates()
df_scored = keyword_metrics.compute_keyword_scores(df_all)
my_utils.save_df(df_scored, "data/processed/scored_keywords.csv")

# Cluster
df_clustered = keyword_clustering.cluster_keywords(df_scored, n = 5)
my_utils.save_df(df_clustered, "data/processed/clustered_keywords.csv")
my_utils.print_top(df_clustered)