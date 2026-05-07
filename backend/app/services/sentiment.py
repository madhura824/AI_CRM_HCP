# backend/app/services/sentiment.py

def fallback_sentiment(text: str):
    text = text.lower()

    if any(w in text for w in ["happy", "satisfied", "good", "great", "success"]):
        return "positive"

    if any(w in text for w in ["not", "no", "refused", "angry", "bad"]):
        return "negative"

    return "neutral"