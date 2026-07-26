import telebot
from telebot import types
from tinydb import TinyDB, Query

# اطلاعات ربات و کانال
TOKEN = "8981068430:AAGOnvNo3656H8E48dUFFgWRQe2rdFDB_48"
CHANNEL_ID = -1004386489690
REQUIRED_INVITES = 3

bot = telebot.TeleBot(TOKEN)
db = TinyDB('database.json')
users = Query()

# ساخت لینک دعوت اختصاصی
def get_invite_link(user_id):
    return f"https://t.me/{bot.get_me().username}?start={user_id}"

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    args = message.text.split()

    # اگر کاربر با لینک دعوت وارد شده
    if len(args) > 1:
        inviter_id = args[1]
        if inviter_id != str(user_id):
            inviter = db.search(users.id == int(inviter_id))
            if inviter:
                invites = inviter[0]['invites'] + 1
                db.update({'invites': invites}, users.id == int(inviter_id))
            else:
                db.insert({'id': int(inviter_id), 'invites': 1})

    # ثبت کاربر در دیتابیس
    if not db.search(users.id == user_id):
        db.insert({'id': user_id, 'invites': 0})

    # دکمه لینک دعوت
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("لینک دعوت اختصاصی من", callback_data="my_link")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "سلام امیر! برای ورود به کانال BANIA باید ۳ نفر دعوت کنی.\n\nروی دکمه زیر بزن:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    data = db.search(users.id == user_id)[0]
    invites = data['invites']

    if call.data == "my_link":
        link = get_invite_link(user_id)
        bot.answer_callback_query(call.id, "لینک اختصاصی شما ساخته شد!")
        bot.send_message(
            call.message.chat.id,
            f"🔗 لینک دعوت اختصاصی شما:\n{link}\n\n"
            f"👥 تعداد دعوت‌های شما: {invites}/{REQUIRED_INVITES}"
        )

        # اگر کاربر به حد نصاب رسید
        if invites >= REQUIRED_INVITES:
            bot.send_message(
                call.message.chat.id,
                f"تبریک! 🎉\nشما به حد نصاب رسیدید.\n\n"
                f"لینک ورود به کانال:\nhttps://t.me/c/{str(CHANNEL_ID)[4:]}"
            )

bot.polling()
