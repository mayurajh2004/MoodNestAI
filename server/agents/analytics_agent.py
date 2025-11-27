from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    # Polarity: -1.0 (negative) to 1.0 (positive)
    # Subjectivity: 0.0 (objective) to 1.0 (subjective)
    return {
        "score": blob.sentiment.polarity,
        "magnitude": blob.sentiment.subjectivity
    }
