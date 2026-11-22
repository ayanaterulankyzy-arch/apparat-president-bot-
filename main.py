
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

NAMES = {
    "a": "aruzhaan",
    "e": "Ерулан",
    "j": "jin",
}

async def name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.split()[0].split("@")[0][1:]
    name = NAMES.get(command)

    await update.message.reply_text(
        f"{name} • 𝐀𝐩𝐩𝐚𝐫𝐚𝐭 𝐏𝐫𝐞𝐳𝐢𝐝𝐞𝐧𝐭𝐚🏛"
    )

app = Application.builder().token(os.environ["BOT_TOKEN"]).build()

for command in NAMES:
    app.add_handler(CommandHandler(command, name_command))

TOKEN = os.environ["BOT_TOKEN"]
HOST = os.environ["RENDER_EXTERNAL_HOSTNAME"]
PORT = int(os.environ.get("PORT", 10000))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"https://{HOST}/{TOKEN}"
)
