import os
from flask import Flask, request
from telegram import Bot, Update

# ======================
# ENV VARIABLES
# ======================
TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x.strip()]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing")

bot = Bot(token=TOKEN)
app = Flask(__name__)


# ======================
# HEALTH CHECK
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

    print("========== NEW UPDATE ==========")
    print(data)

    update = Update.de_json(data, bot)

    if not update.message:
        print("NO MESSAGE FOUND")
        return "OK"

    msg = update.message

    text = msg.text or ""

    print("MESSAGE:", text)

    for gid in GROUP_IDS:
        try:
            print("SENDING TO GROUP:", gid)

            if msg.text:
                bot.send_message(chat_id=gid, text=text)

            elif msg.photo:
                bot.send_photo(chat_id=gid, photo=msg.photo[-1].file_id)

            elif msg.video:
                bot.send_video(chat_id=gid, video=msg.video.file_id)

            elif msg.document:
                bot.send_document(chat_id=gid, document=msg.document.file_id)

            print("SENT SUCCESS:", gid)

        except Exception as e:
            print("SEND ERROR:", e)

    return "OK"


# ======================
# START APP
# ======================
if __name__ == "__main__":
    print("BOT STARTED")

    # SET WEBHOOK AUTOMATICALLY
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"
        bot.set_webhook(url=url)
        print("Webhook set:", url)

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
