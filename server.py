from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

FILE = "chat.json"

ADMIN_ID = 8811147681  # آی‌دی خودت

# ذخیره چت‌ها
def load_chat():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_chat(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

chat = load_chat()


# گرفتن پیام‌ها برای وب اپ
@app.route("/messages")
def messages():
    return jsonify(chat)


# پیام کاربر
@app.route("/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")

    chat.append({
        "role": "user",
        "text": text
    })

    save_chat(chat)
    return {"ok": True}


# پاسخ ادمین (دستی)
@app.route("/admin-reply", methods=["POST"])
def admin_reply():
    data = request.json
    text = data.get("text")

    chat.append({
        "role": "admin",
        "text": text
    })

    save_chat(chat)
    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
