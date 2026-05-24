import os
from flask import Flask, request
from telegram import Bot, Update

TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x]

if not TOKEN:
    raise ValueError("BOT_TOKEN missing")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# -------------------------
# Telegram Webhook Route
# -------------------------
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, bot)

    if update.message:
        msg = update.message

        for gid in GROUP_IDS:
            try:
                if msg.text:
                    bot.send_message(chat_id=gid, text=msg.text)

                elif msg.photo:
                    bot.send_photo(chat_id=gid, photo=msg.photo[-1].file_id)

                elif msg.video:
                    bot.send_video(chat_id=gid, video=msg.video.file_id)

                elif msg.document:
                    bot.send_document(chat_id=gid, document=msg.document.file_id)

            except Exception as e:
                print("ERROR:", e)

    return "OK"


# -------------------------
# Health check route (Render needs this)
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    print("BOT STARTED")

    # IMPORTANT: set webhook automatically
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    if WEBHOOK_URL:
        bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
        print("Webhook set to:", f"{WEBHOOK_URL}/{TOKEN}")

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
