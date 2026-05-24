import os
import requests
from flask import Flask, request
from telegram import Bot, Update

TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x.strip()]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("Missing BOT_TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)


# ======================
# HOME ROUTE
# ======================
@app.route("/", methods=["GET"])
def home():
    return "BOT IS RUNNING"


# ======================
# WEBHOOK
# ======================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("\nNEW UPDATE:", data)

    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    msg = update.message

    print("CHAT ID:", msg.chat.id)
    print("TEXT:", msg.text)

    # reply test
    try:
        bot.send_message(chat_id=msg.chat.id, text="✅ Bot received your message")
    except Exception as e:
        print("PRIVATE ERROR:", e)

    # forward to group
    for gid in GROUP_IDS:
        try:
            print("SENDING TO:", gid)

            bot.send_message(
                chat_id=gid,
                text=f"Forward: {msg.text}"
            )

            print("SUCCESS:", gid)

        except Exception as e:
            print("FAILED:", gid, e)

    return "OK"


# ======================
# START
# ======================
if __name__ == "__main__":
    print("BOT STARTED")

    # 🔥 SAFE WEBHOOK SET (NO ASYNC)
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"

        try:
            requests.get(
                f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}"
            )
            print("Webhook set:", url)
        except Exception as e:
            print("Webhook error:", e)

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
