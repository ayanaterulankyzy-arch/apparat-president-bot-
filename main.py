
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

FOOTER = " • 𝐀𝐩𝐩𝐚𝐫𝐚𝐭 𝐏𝐫𝐞𝐳𝐢𝐝𝐞𝐧𝐭𝐚🏛"

NAMES = {
    "m": "Merey",
    "d": "dilya",
    "e": "Ерулан",
    "aru": "aruzhaan",
    "a": "Айя",
    "za": "закъкъум",
    "ze": "Zekkas",
    "b": "Byirabas",
    "mn": "Monna",
    "c": "cherry kiss",
    "n": "Noyan Olise",
    "ar": "Arabella",
    "i": "indikoosh",
    "da": "Daneshovv",
    "me": "medina",
    "al": "alua",
}


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.effective_message.reply_text(
        "Қош келдіңіз! 🏛\n"
        "Apparat Prezidenta боты іске қосылды."
    )


async def name_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = update.effective_message

    if not message or not message.text:
        return

    command = (
        message.text.split()[0]
        .split("@")[0][1:]
        .lower()
    )

    name = NAMES.get(command)

    if name:
        await message.reply_text(name + FOOTER)
    else:
        await message.reply_text("Мұндай команда жоқ.")


app = Application.builder().token(
    os.environ["BOT_TOKEN"]
).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.COMMAND, name_command)
)

TOKEN = os.environ["BOT_TOKEN"]
HOST = os.environ["RENDER_EXTERNAL_HOSTNAME"]
PORT = int(os.environ.get("PORT", 10000))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"https://{HOST}/{TOKEN}",
)
