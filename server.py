from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8811147681

FILE = "chat.json"

def load_chat():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_chat(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

chat = load_chat()


# ارسال پیام به تلگرام ادمین
def send_to_telegram(user_id, text):
    msg = f"📩 پیام جدید WebApp\n\n🆔 User: {user_id}\n💬 {text}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": ADMIN_ID,
        "text": msg,
        "reply_markup": {
            "force_reply": True
        }
    })


@app.route("/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    user_id = data.get("user_id")

    chat.append({
        "role": "user",
        "text": text,
        "user_id": user_id
    })

    save_chat(chat)

    send_to_telegram(user_id, text)

    return {"ok": True}


@app.route("/messages")
def messages():
    return jsonify(chat)


# وقتی ادمین در تلگرام reply می‌کند
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.json

    if "message" not in update:
        return {"ok": True}

    message = update["message"]

    # فقط ریپلای ادمین
    if "reply_to_message" not in message:
        return {"ok": True}

    if str(message["from"]["id"]) != str(ADMIN_ID):
        return {"ok": True}

    admin_text = message["text"]

    # استخراج user_id از متن پیام قبلی
    original = message["reply_to_message"]["text"]

    try:
        user_id_line = [line for line in original.split("\n") if "User:" in line][0]
        user_id = user_id_line.replace("🆔 User:", "").strip()
    except:
        return {"ok": True}

    chat.append({
        "role": "admin",
        "text": admin_text,
        "user_id": user_id
    })

    save_chat(chat)

    # ارسال جواب به کاربر داخل WebApp
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": user_id,
        "text": f"👨🏻‍💻 پاسخ پشتیبانی:\n\n{admin_text}"
    })

    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
