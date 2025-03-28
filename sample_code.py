from keybert import KeyBERT
import re
import nltk

# Load KeyBERT model
kw_model = KeyBERT()

# Sample product listing
text = """High-quality waterproof Bluetooth speakers with deep bass and long battery life. 
          Perfect for outdoor adventures, beach trips, and home use."""

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters
    return text

# Extract keywords using KeyBERT
def extract_keywords(text, num_keywords=5):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=num_keywords)
    return [kw[0] for kw in keywords]  # Extract just the keyword strings

# Process text
processed_text = preprocess_text(text)
keywords = extract_keywords(processed_text)

# Reordering strategy: Prioritize product-related terms
optimized_keywords = sorted(keywords, key=lambda k: ('bluetooth' in k, 'waterproof' in k), reverse=True)

print("Optimized Keywords:", optimized_keywords)
