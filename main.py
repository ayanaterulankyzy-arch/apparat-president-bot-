
import os
import re
import httpx

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

DEFAULT_NAMES = {
    "a": "aruzhaan",
    "e": "Ерулан",
    "j": "jin",
}


async def db_request(method, params=None, data=None, prefer=None):
    headers = HEADERS.copy()
    if prefer:
        headers["Prefer"] = prefer

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.request(
            method,
            f"{SUPABASE_URL}/rest/v1/bot_names",
            headers=headers,
            params=params,
            json=data,
        )
        response.raise_for_status()

        if response.content:
            return response.json()
        return []


async def get_names(chat_id):
    rows = await db_request(
        "GET",
        params={
            "chat_id": f"eq.{chat_id}",
            "select": "command,display_name",
            "order": "command",
        },
    )

    if not rows:
        defaults = [
            {
                "chat_id": chat_id,
                "command": command,
                "display_name": name,
            }
            for command, name in DEFAULT_NAMES.items()
        ]

        await db_request(
            "POST",
            params={"on_conflict": "chat_id,command"},
            data=defaults,
            prefer="resolution=merge-duplicates,return=representation",
        )

        rows = await db_request(
            "GET",
            params={
                "chat_id": f"eq.{chat_id}",
                "select": "command,display_name",
                "order": "command",
            },
        )

    return rows


async def is_admin(update, context):
    if update.effective_chat.type == "private":
        return False

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id,
    )

    return member.status in ("administrator", "creator")


async def add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("Бұл команданы тек админ қолдана алады.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Қолдану: /add m Меруерт"
        )
        return

    command = context.args[0].lower()
    name = " ".join(context.args[1:]).strip()

    if not re.fullmatch(r"[a-z0-9_]{1,32}", command):
        await update.message.reply_text("Команда тек ағылшын әріптері, сандар немесе _ болуы керек.")
        return

    await get_names(update.effective_chat.id)

    await db_request(
        "POST",
        params={"on_conflict": "chat_id,command"},
        data={
            "chat_id": update.effective_chat.id,
            "command": command,
            "display_name": name,
        },
        prefer="resolution=merge-duplicates,return=representation",
    )

    await update.message.reply_text(f"Қосылды: /{command} → {name}")


async def delete_name(update: Update, context: ContextTypes.DEFAULT_TYPE):


    if len(context.args) != 1:
        await update.message.reply_text("Қолдану: /del m")
        return

    command = context.args[0].lower()

    await get_names(update.effective_chat.id)

    await db_request(
        "DELETE",
        params={
            "chat_id": f"eq.{update.effective_chat.id}",
            "command": f"eq.{command}",
        },
    )

    await update.message.reply_text(f"/{command} өшірілді.")


async def list_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("Бұл команданы тек админ қолдана алады.")
        return

    rows = await get_names(update.effective_chat.id)

    if not rows:
        await update.message.reply_text("Әзірге аттар жоқ.")
        return

    result = "\n".join(
        f"/{row['command']} — {row['display_name']}"
        for row in rows
    )

    await update.message.reply_text(result)


async def name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = (
        update.message.text.split()[0]
        .split("@")[0][1:]
        .lower()
    )

    rows = await get_names(update.effective_chat.id)

    name = next(
        (row["display_name"] for row in rows if row["command"] == command),
        None,
    )

    if not name:
        await update.message.reply_text("Мұндай команда табылмады.")
        return

    await update.message.reply_text(
        f"{name} • 𝐀𝐩𝐩𝐚𝐫𝐚𝐭 𝐏𝐫𝐞𝐳𝐢𝐝𝐞𝐧𝐭𝐚🏛"
    )


app = Application.builder().token(os.environ["BOT_TOKEN"]).build()

app.add_handler(CommandHandler("add", add_name))
app.add_handler(CommandHandler("del", delete_name))
app.add_handler(CommandHandler("list", list_names))

app.add_handler(
    MessageHandler(filters.COMMAND, name_command),
    group=1,
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
