import os
from flask import Flask, request
from telegram import Bot, Update

# =========================
# ENV VARIABLES
# =========================
TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing")

# =========================
# INIT
# =========================
bot = Bot(token=TOKEN)
app = Flask(__name__)

# =========================
# WEBHOOK ROUTE
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("INCOMING:", data)

    update = Update.de_json(data, bot)

    if update.message:
        msg = update.message
        print("MESSAGE RECEIVED:", msg)

        for gid in GROUP_IDS:
            try:
                # TEMP TEST MESSAGE
                bot.send_message(
                    chat_id=gid,
                    text="TEST: message received"
                )
                print("SENT TO:", gid)

            except Exception as e:
                print("SEND ERROR:", e)

    return "OK"


# =========================
# HEALTH CHECK
# =========================
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


# =========================
# SET WEBHOOK ON START
# =========================
def setup_webhook():
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"
        bot.set_webhook(url=url)
        print("Webhook set to:", url)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("BOT STARTED")

    setup_webhook()

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
