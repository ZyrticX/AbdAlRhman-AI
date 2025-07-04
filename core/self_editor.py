import hashlib
import os

def calculate_hash(filepath):
    """احسب بصمة SHA256 لأي ملف"""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def detect_code_change(filepath, old_hash):
    """اكتشف ما إذا تغيّر الملف"""
    if not os.path.exists(filepath):
        return True, None
    new_hash = calculate_hash(filepath)
    return new_hash != old_hash, new_hash

def list_python_files(directory):
    """رجّع كل الملفات .py في مجلد معين ومجلداته الفرعية"""
    py_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))
    return py_files

