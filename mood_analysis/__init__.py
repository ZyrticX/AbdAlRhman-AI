from transformers import pipeline

analyzer = pipeline("text-classification", model="avichr/heBERT_sentiment_analysis")

def get_mood(text: str) -> float:
    result = analyzer(text)[0]
    return 1.0 if result['label'] == 'positive' else -1.0
