from textblob import TextBlob

def analyze_sentiment(text):
    """تحليل المشاعر باستخدام TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        mood = "إيجابي 😊"
    elif polarity < -0.3:
        mood = "سلبي 😞"
    else:
        mood = "محايد 😐"

    return mood

