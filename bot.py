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
    raise ValueError("BOT_TOKEN missing")

bot = Bot(token=TOKEN)
app = Flask(__name__)


# ======================
# HOME
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

    print("\n========== NEW UPDATE ==========")
    print(data)

    update = Update.de_json(data, bot)

    if not update.message:
        print("NO MESSAGE FOUND")
        return "OK"

    msg = update.message

    # ======================
    # 🔥 AUTO SHOW CHAT ID (IMPORTANT)
    # ======================
    print("CHAT ID (USE THIS AS GROUP_ID):", msg.chat.id)
    print("TEXT:", msg.text)

    # ======================
    # TEST PRIVATE REPLY (CHECK BOT WORKS)
    # ======================
    try:
        bot.send_message(
            chat_id=msg.chat.id,
            text="✅ BOT RECEIVED YOUR MESSAGE"
        )
        print("PRIVATE REPLY OK")
    except Exception as e:
        print("PRIVATE ERROR:", repr(e))

    # ======================
    # FORWARD TO GROUPS
    # ======================
    for gid in GROUP_IDS:
        try:
            print("TRY GROUP:", gid)

            result = bot.send_message(
                chat_id=gid,
                text=f"FORWARD: {msg.text}"
            )

            print("SUCCESS GROUP:", gid, "MSG ID:", result.message_id)

        except Exception as e:
            print("FAILED GROUP:", gid)
            print("ERROR:", repr(e))

    return "OK"


# ======================
# START
# ======================
if __name__ == "__main__":
    print("BOT STARTED")

    # SET WEBHOOK
    if WEBHOOK_URL:
        url = f"{WEBHOOK_URL}/webhook"
        bot.set_webhook(url=url)
        print("Webhook set:", url)

    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
