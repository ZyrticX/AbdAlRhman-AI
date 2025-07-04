def detect_intent(text: str) -> str:
    text = text.lower()

    if any(keyword in text for keyword in ["open", "افتح", "اذهب إلى", "visit"]):
        return "open_url"
    elif any(keyword in text for keyword in ["summarize", "تلخيص", "summary", "لخص"]):
        return "summarize"
    elif any(keyword in text for keyword in ["play", "شغل", "استمع", "watch"]):
        return "play_media"
    elif any(keyword in text for keyword in ["search", "ابحث", "جوجل"]):
        return "search"
    elif any(keyword in text for keyword in ["what's your name", "who are you", "ما اسمك", "من أنت", "من تكون"]):
        return "about_ai"
    else:
        return "chat"

