import re
import nltk
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_nltk import Rake

# Load models
kw_model = KeyBERT()

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove special characters
    return text.strip()

# Function to extract keywords using different methods
def extract_keywords(text, method="keybert", num_keywords=5):
    text = preprocess_text(text)
    
    if method == "keybert":
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=num_keywords)
        return [kw[0] for kw in keywords]

    elif method == "tfidf":
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        X = vectorizer.fit_transform([text])
        feature_array = vectorizer.get_feature_names_out()
        tfidf_scores = X.toarray().flatten()
        sorted_indices = tfidf_scores.argsort()[::-1]
        return [feature_array[i] for i in sorted_indices[:num_keywords]]

    elif method == "rake":
        rake = Rake()
        rake.extract_keywords_from_text(text)
        return rake.get_ranked_phrases()[:num_keywords]

    else:
        raise ValueError("Invalid method. Choose from: 'keybert', 'tfidf', 'rake'.")

# Function to reorder keywords based on priority (Customizable)
def reorder_keywords(keywords, priority_terms=None):
    if priority_terms:
        return sorted(keywords, key=lambda k: any(term in k for term in priority_terms), reverse=True)
    return keywords

# Sample product description
text = """High-quality waterproof Bluetooth speakers with deep bass and long battery life. 
          Perfect for outdoor adventures, beach trips, and home use."""

# Choose keyword extraction method
method = "keybert"  # Change to "tfidf" or "rake" as needed

# Extract and reorder keywords
keywords = extract_keywords(text, method=method, num_keywords=5)
priority_terms = ["bluetooth", "waterproof"]  # Customize based on product type
optimized_keywords = reorder_keywords(keywords, priority_terms)

# Output
print(f"Method: {method}")
print("Optimized Keywords:", optimized_keywords)
