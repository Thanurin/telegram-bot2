import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update

TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x.strip()]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN)
app = Flask(__name__)

print("BOT STARTED")


@app.route("/", methods=["GET"])
def home():
    return "BOT IS RUNNING"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("\nWEBHOOK HIT")
    print(data)

    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    msg = update.message

    print("CHAT ID:", msg.chat.id)
    print("TEXT:", msg.text)

    # -------------------------
    # FIX: run async safely
    # -------------------------
    async def process():
        await bot.send_message(
            chat_id=msg.chat.id,
            text="✅ Bot received your message"
        )

        for gid in GROUP_IDS:
            await bot.send_message(
                chat_id=gid,
                text=f"FORWARD: {msg.text}"
            )

    asyncio.run(process())

    return "OK"


if __name__ == "__main__":
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"

        import requests
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}"
        )

        print("Webhook set:", url)

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
