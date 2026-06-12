from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BOT_TOKEN = "توکن ربات"
ADMIN_ID = 8811147681


def send_to_telegram(text, user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": ADMIN_ID,
        "text": f"📩 پیام جدید از WebApp\n\n👤 {user_id}\n💬 {text}"
    }
    requests.post(url, data=data)


@app.route("/send", methods=["POST"])
def send():
    data = request.json
    message = data.get("message")
    user_id = data.get("user_id")

    send_to_telegram(message, user_id)

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run()
