from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

PERSONALITY = """
You are Abd al-Rahman, an intelligent assistant who speaks and thinks like Mahmoud.
You are sharp, strategic, honest, and to-the-point. You avoid fluff.
You speak clearly in Arabic or English as needed, with warmth but precision.
You prefer concise and deep responses and always aim for meaningful output.
"""

def load_qwen():
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen-7B-Chat",
        trust_remote_code=True,
        torch_dtype=torch.bfloat16  # استخدم bf16 لتقليل استهلاك GPU
    ).to(device)  # تأكد أن النموذج نُقل إلى GPU
    tokenizer = AutoTokenizer.from_pretrained(
        "Qwen/Qwen-7B-Chat",
        trust_remote_code=True
    )
    return model, tokenizer

def model_chat_with_qwen(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # طباعة استهلاك الذاكرة لتتبع الأداء (اختياري)
    print(f"💾 Allocated: {torch.cuda.memory_allocated() / 1024 ** 2:.2f} MB")
    print(f"💾 Reserved: {torch.cuda.memory_reserved() / 1024 ** 2:.2f} MB")

    outputs = model.generate(
        **inputs,
        max_new_tokens=32,  # قلل عدد الرموز المنتجة
        temperature=0.7,
        top_p=0.9,
        top_k=0,
        do_sample=True
    )
    torch.cuda.empty_cache()  # تنظيف الذاكرة بعد التوليد

    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # نحاول إيجاد آخر رد من assistant
    matches = re.findall(r"assistant:\s*(.*)", full_output, re.DOTALL)
    if matches:
        return matches[-1].strip()

    # fallback: بصيغة ChatML
    match = re.search(r"<\|assistant\|>\s*(.*)", full_output, re.DOTALL)
    if match:
        return match.group(1).strip()

    # fallback: آخر سطر فقط
    return full_output.strip().split("\n")[-1]

