from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
from tools.intent_analyzer import detect_intent
from tools.time_context import extract_time_context
import os

# إيقاف حفظ واسترجاع الذاكرة مؤقتًا
save_interaction = lambda user, assistant: None
retrieve_recent_memories = lambda: []

app = Flask(__name__)
CORS(app, supports_credentials=True)

ALLOWED_ORIGIN = "https://abd-alrhman-frontend.vercel.app"

model = None
tokenizer = None

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response

@app.route("/api", methods=["OPTIONS"])
def handle_options():
    response = make_response()
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response, 204

@app.route("/api", methods=["POST"])
def api():
    global model, tokenizer

    if model is None or tokenizer is None:
        print("🚀 Loading model to CUDA...")
        model_name = "Qwen/Qwen-7B-Chat"
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).cuda()

    try:
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

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

