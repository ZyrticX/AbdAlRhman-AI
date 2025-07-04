from datetime import datetime, timedelta
import re

def extract_time_context(text):
    now = datetime.now()
    text = text.lower()
    
    if "الآن" in text or "حالياً" in text:
        return now
    
    if "أمس" in text:
        return now - timedelta(days=1)
    
    if "غداً" in text or "بكرا" in text:
        return now + timedelta(days=1)
    
    match = re.search(r"منذ (\d+) يوم", text)
    if match:
        days = int(match.group(1))
        return now - timedelta(days=days)
    
    match = re.search(r"بعد (\d+) يوم", text)
    if match:
        days = int(match.group(1))
        return now + timedelta(days=days)

    return None  # لم يتم التعرف على سياق زمني

# مثال للاختبار
if __name__ == "__main__":
    print(extract_time_context("أعطني أخبار أمس"))

