from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from core.model import model_chat_with_qwen
from tools.memory_manager import save_interaction, retrieve_recent_memories
from tools.intent_analyzer import detect_intent
from tools.time_context import extract_time_context

app = Flask(__name__)

# ✅ CORS يدوي + تلقائي
CORS(app, supports_credentials=True)

# ❗️اجعل Vercel دومينك الأساسي هنا
ALLOWED_ORIGIN = "https://abd-alrhman-frontend.vercel.app"

# تحميل النموذج لاحقاً
model = None
tokenizer = None

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response

@app.route("/api", methods=["POST", "OPTIONS"])
def api():
    if request.method == "OPTIONS":
        return make_response(('', 204))

    if model is None or tokenizer is None:
        return jsonify({"error": "Model not loaded"}), 503

    data = request.get_json()
    msg = data.get("message", "")
    if not msg:
        return jsonify({"error": "Empty message"}), 400

    print("🔍 Intent:", detect_intent(msg))
    time_ctx = extract_time_context(msg)
    if time_ctx:
        print("🕒 Time context:", time_ctx)

    memory_context = "\n".join(
        [f"user: {u}\nassistant: {a}" for u, a in reversed(retrieve_recent_memories())]
    )
    memory_lines = memory_context.strip().split("\n")[-2:]
    memory_context_trimmed = "\n".join(memory_lines)

    PERSONALITY = """
    You are Abd al-Rahman, an intelligent assistant who speaks and thinks like Mahmoud.
    You are sharp, strategic, honest, and to-the-point. You avoid fluff.
    You speak clearly in Arabic or English as needed, with warmth but precision.
    You prefer concise and deep responses and always aim for meaningful output.
    """
    
    prompt = f"{PERSONALITY}\n{memory_context_trimmed}\nuser: {msg}\nassistant:"
    reply = model_chat_with_qwen(model, tokenizer, prompt)

    save_interaction(msg, reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("🚀 Loading model to CUDA...")
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat", device_map="auto", trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat", trust_remote_code=True)
    print("✅ Abd al-Rahman API is ready at http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

