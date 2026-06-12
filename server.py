from flask import Flask, request, jsonify
import json
import os
import requests

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


# ذخیره پیام کاربر از WebApp
@app.route("/send", methods=["POST"])
def send():
    data = request.json
    text = data["text"]
    user_id = data["user_id"]

    chat.append({
        "role": "user",
        "text": text,
        "user_id": user_id
    })

    save_chat(chat)

    # ارسال به تلگرام ادمین با دکمه جواب
    send_to_admin(text, user_id)

    return {"ok": True}


# لیست پیام‌ها برای WebApp
@app.route("/messages")
def messages():
    return jsonify(chat)


# ارسال به تلگرام ادمین با دکمه ریپلای
def send_to_admin(text, user_id):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": ADMIN_ID,
        "text": f"📩 پیام جدید\n\n🆔 {user_id}\n💬 {text}",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "💬 پاسخ به این کاربر",
                        "callback_data": f"reply:{user_id}"
                    }
                ]
            ]
        }
    })


# پاسخ ادمین از تلگرام
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.json

    if "callback_query" in update:
        cq = update["callback_query"]
        data = cq["data"]

        if data.startswith("reply:"):
            user_id = data.split(":")[1]

            # درخواست جواب از ادمین
            send_telegram_message(
                ADMIN_ID,
                f"✍️ پاسخ خود را برای کاربر {user_id} ارسال کنید (Reply کنید)"
            )

            # ذخیره حالت انتظار (ساده)
            save_pending(user_id)

    if "message" in update:
        msg = update["message"]

        if str(msg["from"]["id"]) != str(ADMIN_ID):
            return {"ok": True}

        # اگر reply بود → ارسال جواب
        if "reply_to_message" in msg:
            admin_text = msg["text"]

            pending = load_pending()

            if not pending:
                return {"ok": True}

            user_id = pending[-1]

            chat.append({
                "role": "admin",
                "text": admin_text,
                "user_id": user_id
            })

            save_chat(chat)

            # ارسال به کاربر
            send_user(user_id, admin_text)

            clear_pending()

    return {"ok": True}


def send_user(user_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": user_id,
        "text": f"👨🏻‍💻 پاسخ پشتیبانی:\n\n{text}"
    })


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })


# ساده‌ترین سیستم pending
def save_pending(user_id):
    with open("pending.json", "w") as f:
        json.dump({"user_id": user_id}, f)

def load_pending():
    try:
        with open("pending.json", "r") as f:
            return json.load(f)["user_id"]
    except:
        return None

def clear_pending():
    if os.path.exists("pending.json"):
        os.remove("pending.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
