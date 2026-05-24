import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

GROUP_IDS = [int(x) for x in os.getenv("GROUP_ID", "").split(",") if x]

async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg:
        return

    for gid in GROUP_IDS:
        try:
            if msg.text:
                await context.bot.send_message(gid, msg.text)
            elif msg.photo:
                await context.bot.send_photo(gid, msg.photo[-1].file_id)
            elif msg.video:
                await context.bot.send_video(gid, msg.video.file_id)
            elif msg.document:
                await context.bot.send_document(gid, msg.document.file_id)
        except Exception as e:
            print("ERROR:", e)

def main():
    print("BOT STARTED")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward))

    app.run_polling()

if __name__ == "__main__":
    main()