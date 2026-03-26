import telebot  # تم تصحيح الحرف الكبير هنا
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. إعداد السيرفر لضمان عمل البوت على Render
# تم تسمية المتغير 'app' ليتوافق مع أمر gunicorn main:app
app = Flask(__name__)

@app.route('/')
def home(): 
    return "Bot is Online and Running!"

def run_flask():
    # الحصول على المنفذ من إعدادات Render أو استخدام 8080 كافتراضي
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت والروابط الأساسية
API_TOKEN = '8788993987:AAGNz5XTpcA14szp7b-hFlueFFUIzuPyd88'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_ID = 8578766174
DB_FILE = "users.txt"

# الرابط الربحي الموحد
MY_LINK = "https://t.co/P0rOZubZgJ"

# دالة حفظ المشتركين
def save_user(user_id):
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: pass
    with open(DB_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(DB_FILE, "a") as f:
            f.write(str(user_id) + "\n")

# أمر البداية /start
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    
    # أزرار الروابط (Inline Keyboard)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🎡 عجلة الحظ", url=MY_LINK),
        types.InlineKeyboardButton("🔑 إدخال كود الهدية", url=MY_LINK),
        types.InlineKeyboardButton("🎯 مهام سريعة", url=MY_LINK),
        types.InlineKeyboardButton("🏆 قائمة المتصدرين", url=MY_LINK),
        types.InlineKeyboardButton("🔫 شحن شدات ببجي", url=MY_LINK),
        types.InlineKeyboardButton("💎 جواهر فري فاير", url=MY_LINK),
        types.InlineKeyboardButton("🎁 صندوق عشوائي", url=MY_LINK),
        types.InlineKeyboardButton("💳 بطاقات جوجل", url=MY_LINK),
        types.InlineKeyboardButton("⚡ ربح نقاط سريع", url=MY_LINK),
        types.InlineKeyboardButton("📲 تطبيقات مدفوعة", url=MY_LINK)
    ]
    markup.add(*btns)
    
    # القائمة السفلية (Reply Keyboard)
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add('🏠 القائمة الرئيسية', '👤 حسابي')
    reply_markup.add('🚀 دعوة صديق', '📞 الدعم الفني')
    
    welcome_text = (
        f"أهلاً بك {message.from_user.first_name} في بوت الجوائز الأكبر! 🏆\n\n"
        "يمكنك الآن جمع النقاط واستبدالها بالهدايا والشحنات مجاناً.\n"
        "اختر من الأقسام المتوفرة أدناه للبدء 👇"
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=reply_markup)
    bot.send_message(message.chat.id, "📢 الأقسام والخدمات المتاحة:", reply_markup=markup)

# ميزة الإذاعة للآدمن
@bot.message_handler(commands=['send'])
def broadcast_command(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "اكتب الرسالة التي تريد توزيعها على الجميع:")
        bot.register_next_step_handler(msg, perform_broadcast)
    else:
        bot.send_message(message.chat.id, "⚠️ عذراً، هذا الأمر مخصص لمدير البوت فقط.")

def perform_broadcast(message):
    if not os.path.exists(DB_FILE):
        bot.send_message(ADMIN_ID, "❌ لا يوجد مشتركين بعد.")
        return
    with open(DB_FILE, "r") as f:
        users = f.read().splitlines()
    count = 0
    for user in users:
        try:
            bot.send_message(user, message.text)
            count += 1
        except:
            continue
    bot.send_message(ADMIN_ID, f"✅ تمت الإذاعة بنجاح لـ {count} مشترك.")

# تشغيل السيرفر والبوت معاً
if __name__ == "__main__":
    # تشغيل Flask في الخلفية
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    print("Bot is starting...")
    # تشغيل البوت بشكل مستمر
    bot.infinity_polling()
