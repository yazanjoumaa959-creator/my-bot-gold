import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

API_TOKEN = '8788993987:AAGNz5XTpcA14szp7b-hFlueFFUIzuPyd88'
ADMIN_ID = 8578766174  
bot = telebot.TeleBot(API_TOKEN)
DB_FILE = "users.txt"

def save_user(user_id):
    if not os.path.exists(DB_FILE): open(DB_FILE, "w").close()
    with open(DB_FILE, "r+") as f:
        users = f.read().splitlines()
        if str(user_id) not in users: f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("💰 ابدأ كسب النقاط الآن", url="https://encyclopediainsoluble.com/zkwsxfxbs7?key=7ea007649e568f3e7a8150dc4bb54f02")
    btn2 = types.InlineKeyboardButton("🎮 قسم ألعاب ومسابقات", url="https://encyclopediainsoluble.com/92/8a/73/928a730ca6c2029d5a531dee6ec1efdf.js")
    btn_ref = types.InlineKeyboardButton("👥 دعوة صديق (اربح 1$)", url="Https://beta.publishers.adsterra.com/referral/xt8ah9W31d")
    inline_markup.add(btn1, btn2, btn_ref)
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(types.KeyboardButton('🏠 القائمة الرئيسية'), types.KeyboardButton('👤 حسابي'))
    bot.send_message(message.chat.id, f"أهلاً بك {message.from_user.first_name}! 🏆", reply_markup=reply_markup)
    bot.send_message(message.chat.id, "اختر من الخيارات أدناه:", reply_markup=inline_markup)

@bot.message_handler(commands=['send'])
def broadcast(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "اكتب رسالة الإذاعة:")
        bot.register_next_step_handler(msg, send_to_all)

def send_to_all(message):
    with open(DB_FILE, "r") as f: users = f.read().splitlines()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except: continue
    bot.send_message(ADMIN_ID, f"✅ تم الإرسال إلى {count} مشترك.")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
