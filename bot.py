import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8454786447:AAG6nrgSpE-jU77B4fnsnM6unQFozzt3zxw"
CHANNEL_USERNAME = "@waserecords_et"
OWNER_ID = 7230332671

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Private bot check
    if user_id != OWNER_ID:
        await update.message.reply_text("⛔ ይህ ቦት የግል ነው")
        return

    # Force Join check
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status not in ["member", "administrator", "creator"]:
        await update.message.reply_text(
            "🔔 ቦቱን ለመጠቀም ቻናሉን መቀላቀል አለብህ\n"
            "👉 https://t.me/waserecords_et"
        )
        return

    await update.message.reply_text("✅ እንኳን ደህና መጣህ!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
