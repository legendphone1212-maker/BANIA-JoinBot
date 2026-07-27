import telebot
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from tinydb import TinyDB, Query

BOT_TOKEN = "8981068430:AAGOnvNo3656H8E48dUFFgWRQe2rdFDB_48"
CHANNEL_ID = -1004386489690
BOT_USERNAME = "BANIA_JoinBot"
OWNER_ID = 305765061

bot = telebot.TeleBot(BOT_TOKEN)

db = TinyDB("database.json")
Users = Query()

class FakeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_fake_server():
    server = HTTPServer(("0.0.0.0", 10000), FakeHandler)
    server.serve_forever()

threading.Thread(target=run_fake_server).start()

def is_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def get_ref_link(user_id):
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    args = message.text.split()
    if len(args) > 1:
        ref = args[1]
        if ref != str(user_id):
            inviter = int(ref)
            record = db.get(Users.user_id == inviter)
            if record:
                db.update({"invites": record["invites"] + 1}, Users.user_id == inviter)
            else:
                db.insert({"user_id": inviter, "invites": 1})

    if not db.get(Users.user_id == user_id):
        db.insert({"user_id": user_id, "invites": 0})

    bot.reply_to(message,
        "سلام! برای ورود به کانال BANIA باید ۳ نفر را دعوت کنی.\n\n"
        f"لینک اختصاصی تو:\n{get_ref_link(user_id)}"
    )

# -----------------------------
# هندلر واقعی و تضمینی /clear
# -----------------------------
@bot.message_handler(func=lambda m: m.text.startswith('/clear'))
def clear_channel(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ شما اجازه اجرای این دستور را ندارید.")
        return

    bot.reply_to(message, "⏳ در حال پاکسازی پیام‌های کانال...")

    try:
        messages = bot.get_chat_history(CHANNEL_ID, limit=100)
        for msg in messages:
            try:
                bot.delete_message(CHANNEL_ID, msg.message_id)
            except:
                pass

        bot.send_message(message.chat.id, "✅ تمام پیام‌های کانال پاک شدند.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ خطا در پاکسازی: {e}")

# -----------------------------
# هندلر پیام‌های معمولی
# -----------------------------
@bot.message_handler(func=lambda m: not m.text.startswith('/clear'))
def handle_all(message):
    user_id = message.from_user.id

    if not is_member(user_id):
        bot.reply_to(message,
            "برای استفاده از ربات باید عضو کانال BANIA باشی.\n\n"
            "لینک کانال:\nhttps://t.me/+something"
        )
        return

    record = db.get(Users.user_id == user_id)
    invites = record["invites"]

    if invites < 3:
        bot.reply_to(message,
            f"تو تا الان {invites} نفر دعوت کردی.\n"
            "برای ورود به کانال باید ۳ نفر را دعوت کنی.\n\n"
            f"لینک اختصاصی تو:\n{get_ref_link(user_id)}"
        )
        return

    bot.reply_to(message,
        "دعوت‌ها کامل شد! 🎉\n"
        "لینک ورود به کانال:\nhttps://t.me/+something"
    )

bot.infinity_polling()
