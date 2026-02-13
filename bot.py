import logging
import random
import string
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ====== YOUR CONFIG ======
BOT_TOKEN = "8454786447:AAG6nrgSpE-jU77B4fnsnM6unQFozzt3zxw"
STORAGE_CHANNEL_ID = -1003823527569
FORCE_JOIN_CHANNEL = "@WaseRecords_et"  # without https://t.me/
ADMIN_ID = 7230332671
# ==========================

logging.basicConfig(level=logging.INFO)

file_store = {}

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        code = context.args[0]
        user = update.effective_user

        # Force Join Check
        try:
            member = await context.bot.get_chat_member(f"@{FORCE_JOIN_CHANNEL}", user.id)
            if member.status in ["left", "kicked"]:
                await update.message.reply_text(
                    f"🚫 መጀመሪያ channel ይቀላቀሉ\n👉 https://t.me/{FORCE_JOIN_CHANNEL}"
                )
                return
        except:
            await update.message.reply_text("Channel check error.")
            return

        if code in file_store:
            msg_id = file_store[code]
            await context.bot.copy_message(
                chat_id=user.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id
            )
        else:
            await update.message.reply_text("❌ Link invalid.")
    else:
        await update.message.reply_text("👋 ፋይል ላክ እኔ link እሰጥሃለሁ.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Upload ለአንተ ብቻ ይፈቀዳል.")
        return

    sent = await context.bot.copy_message(
        chat_id=STORAGE_CHANNEL_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

    code = generate_code()
    file_store[code] = sent.message_id

    link = f"https://t.me/{context.bot.username}?start={code}"
    await update.message.reply_text(f"✅ Link:\n{link}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_file))

    print("Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
