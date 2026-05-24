import os
from flask import Flask, request
from telegram import Bot, Update

# ======================
# ENV
# ======================
TOKEN = os.getenv("BOT_TOKEN")
GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x.strip()]
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing")

bot = Bot(token=TOKEN)
app = Flask(__name__)


# ======================
# HOME ROUTE
# ======================
@app.route("/", methods=["GET"])
def home():
    return "BOT IS RUNNING"


# ======================
# WEBHOOK ROUTE
# ======================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    print("\n=== NEW UPDATE ===")
    print(data)

    update = Update.de_json(data, bot)

    if not update.message:
        return "OK"

    msg = update.message

    print("CHAT ID (USE THIS FOR GROUP_ID):", msg.chat.id)
    print("MESSAGE:", msg.text)

    # ----------------------
    # TEST: reply to sender
    # ----------------------
    try:
        bot.send_message(
            chat_id=msg.chat.id,
            text="✅ Bot received your message"
        )
    except Exception as e:
        print("PRIVATE SEND ERROR:", e)

    # ----------------------
    # FORWARD TO GROUPS
    # ----------------------
    for gid in GROUP_IDS:
        try:
            print("Sending to group:", gid)

            bot.send_message(
                chat_id=gid,
                text=f"Forward: {msg.text}"
            )

            print("SUCCESS GROUP:", gid)

        except Exception as e:
            print("FAILED GROUP:", gid)
            print("ERROR:", repr(e))

    return "OK"


# ======================
# START SERVER
# ======================
if __name__ == "__main__":
    print("BOT STARTED")

    # SAFE WEBHOOK SETUP (NO ASYNC ERROR)
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"

        try:
            bot.set_webhook(url=url)
        except Exception as e:
            print("Webhook error:", e)

        print("Webhook set:", url)

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
