
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = " ".join(context.args).strip()

    if not name:
        await update.message.reply_text("Қолдану: /a name")
        return

    await update.message.reply_text(
        f"{name} • 𝐀𝐩𝐩𝐚𝐫𝐚𝐭 𝐏𝐫𝐞𝐳𝐢𝐝𝐞𝐧𝐭𝐚🏛"
    )

TOKEN = os.environ["BOT_TOKEN"]
HOST = os.environ["RENDER_EXTERNAL_HOSTNAME"]
PORT = int(os.environ.get("PORT", 10000))

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("a", start))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"https://{HOST}/{TOKEN}"
)
