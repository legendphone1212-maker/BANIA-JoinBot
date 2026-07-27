import telebot
from telebot import types

BOT_TOKEN = "توکن_ربات_اینجا"
CHANNEL_ID = -1001234567890   # آیدی کانال BANIA
OWNER_ID = 305765061          # آیدی خودت

bot = telebot.TeleBot(BOT_TOKEN)

# ---------------------------
# هندلر دستور /start
# ---------------------------
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id

    # لینک اختصاصی دعوت
    invite_link = f"https://t.me/BANIA_JoinBot?start={user_id}"

    bot.reply_to(
        message,
        f"سلام! برای ورود به کانال BANIA باید ۳ نفر را دعوت کنی.\n\n"
        f"لینک اختصاصی تو:\n{invite_link}"
    )

# ---------------------------
# هندلر دستور /clear
# ---------------------------
@bot.message_handler(commands=['clear'])
def clear_channel(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ شما اجازه اجرای این دستور را ندارید.")
        return

    bot.reply_to(message, "⏳ در حال پاکسازی پیام‌های کانال...")

    try:
        updates = bot.get_updates()

        for update in updates:
            if update.channel_post and update.channel_post.chat.id == CHANNEL_ID:
                msg_id = update.channel_post.message_id
                try:
                    bot.delete_message(CHANNEL_ID, msg_id)
                except:
                    pass

        bot.send_message(message.chat.id, "✅ تمام پیام‌های کانال پاک شدند.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ خطا در پاکسازی: {e}")

# ---------------------------
# اجرای ربات
# ---------------------------
bot.infinity_polling()
