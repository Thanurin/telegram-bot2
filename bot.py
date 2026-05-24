import os
from flask import Flask, request
from telegram import Bot, Update

# -------------------------
# ENV VARIABLES
# -------------------------
TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("BOT_TOKEN missing")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# -------------------------
# WEBHOOK ROUTE
# -------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, bot)

    if update.message:
        msg = update.message

        for gid in GROUP_IDS:
            try:
                # TEXT
                if msg.text:
                    bot.send_message(chat_id=gid, text=msg.text)

                # PHOTO
                if msg.photo:
                    bot.send_photo(chat_id=gid, photo=msg.photo[-1].file_id)

                # VIDEO
                if msg.video:
                    bot.send_video(chat_id=gid, video=msg.video.file_id)

                # DOCUMENT
                if msg.document:
                    bot.send_document(chat_id=gid, document=msg.document.file_id)

            except Exception as e:
                print("ERROR SENDING:", e)

    return "OK"


# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


# -------------------------
# START SERVER
# -------------------------
if __name__ == "__main__":
    print("BOT STARTED")

    # SET WEBHOOK AUTOMATICALLY
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"
        result = bot.set_webhook(url=url)
        print("Webhook set:", result)
        print("Webhook URL:", url)

    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
