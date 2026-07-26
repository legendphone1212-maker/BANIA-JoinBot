import telebot
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# -----------------------------
# تنظیمات ربات
# -----------------------------
BOT_TOKEN = "8981068430:AAGOnvNo3656H8E48dUFFgWRQe2rdFDB_48"
CHANNEL_ID = -1004386489690   # آیدی کانال BANIA

bot = telebot.TeleBot(BOT_TOKEN)

# -----------------------------
# سرور فیک برای Render (اجباری)
# -----------------------------
class FakeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_fake_server():
    server = HTTPServer(("0.0.0.0", 10000), FakeHandler)
    server.serve_forever()

threading.Thread(target=run_fake_server).start()

# -----------------------------
# چک عضویت کاربر در کانال
# -----------------------------
def is_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# -----------------------------
# هندلر پیام‌ها
# -----------------------------
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    user_id = message.from_user.id

    if not is_member(user_id):
        bot.reply_to(message,
            "برای استفاده از ربات باید عضو کانال BANIA باشی.\n\n"
            "لینک کانال:\nhttps://t.me/+something"
        )
        return

    bot.reply_to(message, "عضویتت تایید شد ✔️")

# -----------------------------
# اجرای ربات
# -----------------------------
bot.infinity_polling()
