from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
from core.model import model_chat_with_qwen
from tools.memory_manager import save_interaction, retrieve_recent_memories
from tools.intent_analyzer import detect_intent
from tools.time_context import extract_time_context

app = Flask(__name__)

# السماح بالدومين الصحيح فقط
ALLOWED_ORIGIN = "https://abd-alrhman-frontend.vercel.app"

# تفعيل CORS عام
CORS(app, supports_credentials=True)

# ✅ التعامل الصريح مع preflight requests لمنصة Render
@app.route('/api', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response, 204

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response

# تحميل النموذج (سيتم تحميله عند أول طلب)
model = None
tokenizer = None

@app.route("/api", methods=["POST", "OPTIONS"])
def api():
    if request.method == "OPTIONS":
        return make_response(('', 204))

    global model, tokenizer
    if model is None or tokenizer is None:
        model, tokenizer = model_chat_with_qwen()

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

    full_prompt = f"{PERSONALITY}\n{memory_context_trimmed}\nuser: {msg}\nassistant:"
    input_ids = tokenizer(full_prompt, return_tensors="pt").input_ids.cuda()
    output = model.generate(input_ids, max_new_tokens=200)
    response_text = tokenizer.decode(output[0], skip_special_tokens=True)

    answer = response_text.split("assistant:")[-1].strip()
    save_interaction(msg, answer)

    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

