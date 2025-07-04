import sys
import time
import re
from urllib.parse import urlparse
from datetime import datetime, timedelta

sys.path.append("/data/python_pkgs")

from transformers import AutoModelForCausalLM, AutoTokenizer
from core.model import load_qwen, model_chat_with_qwen
from tools.browser import browse
from tools.summarizer import summarize_page
from tools.intent_analyzer import detect_intent
from core.self_editor import calculate_hash, detect_code_change, list_python_files
from tools.time_context import extract_time_context
from tools.memory_manager import save_interaction, retrieve_recent_memories, init_chat_memory_db

# إعداد قاعدة البيانات
init_chat_memory_db()

# ==============================
# Configuration & Constants
# ==============================

file_hashes = {f: calculate_hash(f) for f in list_python_files(".")}
URL_REGEX = r"https?://[\w\-\./?&=#%]+"

PERSONALITY = """
You are Abd al-Rahman, an intelligent assistant who speaks and thinks like Mahmoud.
You are sharp, strategic, honest, and to-the-point. You avoid fluff.
You speak clearly in Arabic or English as needed, with warmth but precision.
You prefer concise and deep responses and always aim for meaningful output.
"""

# ==============================
# Qwen Model Integration
# ==============================

def load_qwen():
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen-7B-Chat",
        device_map="auto",
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "Qwen/Qwen-7B-Chat",
        trust_remote_code=True
    )
    return model, tokenizer

# ==============================
# Main Function
# ==============================

def main():
    print("\n✅ Abd al-Rahman is running... Loading model to CUDA\n")
    model, tokenizer = load_qwen()

    while True:
        user_input = sys.stdin.buffer.readline().decode('utf-8', errors='replace').strip()

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if not user_input:
            print("❗ Please type a command.")
            continue

        # استخراج سياق زمني إن وُجد
        time_context = extract_time_context(user_input)
        if time_context:
            print(f"⏳ Time context detected: {time_context.strftime('%Y-%m-%d')}")

        # فحص ذاتي للكود
        for f, old_hash in file_hashes.items():
            changed, new_hash = detect_code_change(f, old_hash)
            if changed:
                print(f"⚠️ File changed: {f} — reload or review needed.")
                file_hashes[f] = new_hash

        # تحليل النية
        intent = detect_intent(user_input)
        print(f"🔍 Detected intent: {intent}")

        # التعامل مع النية
        if intent == "open_url":
            print("🌐 Opening Google page...")
            browse("https://www.google.com")

        elif intent == "summarize":
            print("🧠 Summarizing Al Jazeera...")
            summary = summarize_page("https://www.aljazeera.net")
            print("📄 News Summary:\n", summary)

        elif intent == "play_media":
            print("🔊 (Coming soon) Play media feature not implemented yet.")

        elif intent == "search":
            print("🔍 (Coming soon) Smart search not implemented yet.")

        elif intent == "about_ai":
            print("🤖 My name is Abd al-Rahman. I'm your intelligent assistant, constantly learning and evolving to serve you better.")

        else:
            print("🔄 Generating response from Qwen...")

            # 🧠 استرجاع الذكريات
            recent_memories = retrieve_recent_memories()
            memory_context = "\n".join([f"user: {u}\nassistant: {a}" for u, a in reversed(recent_memories)])

            # قص التاريخ إلى آخر سطر واحد فقط لتقليل الاستهلاك
            memory_lines = memory_context.strip().split("\n")[-2:]
            memory_context_trimmed = "\n".join(memory_lines)
            full_prompt = f"{PERSONALITY}\n{memory_context_trimmed}\nuser: {user_input}\nassistant:"

            # 🧠 التفاعل مع Qwen
            response = model_chat_with_qwen(model, tokenizer, full_prompt)
            print(f"\n🤖: {response}\n")

            # 🧠 حفظ التفاعل في الذاكرة
            save_interaction(user_input, response)

            # فتح رابط تلقائي إذا تم اكتشافه
            match = re.search(URL_REGEX, response)
            if match:
                url = match.group(0)
                print(f"🌐 Opening link automatically: {url}")
                try:
                    browse(url)
                except Exception as e:
                    print(f"❌ Error opening link: {e}")

if __name__ == "__main__":
    main()

