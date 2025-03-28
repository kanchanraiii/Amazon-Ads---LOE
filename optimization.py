import pandas as pd
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from transformers import pipeline

# Load product data
df = pd.read_csv("amazon_products.csv")

# Load NLP model for keyword extraction (Example: BERT-based)
keyword_extractor = pipeline("feature-extraction", model="bert-base-uncased")

def rank_keywords(text):
    words = word_tokenize(text.lower())
    freq = Counter(words)
    ranked_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw[0] for kw in ranked_keywords][:10]  # Top 10 keywords

# Apply keyword ranking and rearrangement
df["Keywords"] = df["Description"].apply(rank_keywords)

# Rearranging description to prioritize high-ranking keywords
def optimize_description(description, keywords):
    words = word_tokenize(description)
    reordered = sorted(words, key=lambda x: keywords.index(x) if x in keywords else len(words))
    return " ".join(reordered)

df["Optimized_Description"] = df.apply(lambda row: optimize_description(row["Description"], row["Keywords"]), axis=1)

# Save optimized data
df.to_csv("optimized_products.csv", index=False)
