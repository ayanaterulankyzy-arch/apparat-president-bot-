
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "aruzhaan • 𝐀𝐩𝐩𝐚𝐫𝐚𝐭 𝐏𝐫𝐞𝐳𝐢𝐝𝐞𝐧𝐭𝐚🏛"
    )

app = Application.builder().token(
    os.environ["BOT_TOKEN"]
).build()

app.add_handler(CommandHandler("a", start))

app.run_polling()
