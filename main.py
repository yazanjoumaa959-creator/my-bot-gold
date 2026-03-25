import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# 1. إعداد السيرفر لضمان عمل البوت على Render 24/7
app = Flask('')
@app.route('/')
def home(): return "Bot is Online and Running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 2. إعدادات البوت والروابط الأساسية
API_TOKEN = '8788993987:AAGNz5XTpcA14szp7b-hFlueFFUIzuPyd88'
bot = telebot.TeleBot(API_TOKEN)
ADMIN_ID = 8578766174
DB_FILE = "users.txt"

# روابطك التي طلبتها
LINK_1 = "https://encyclopediainsoluble.com/zkwsxfxbs7?key=7ea007649e568f3e7a8150dc4bb54f02"
LINK_2 = "https://encyclopediainsoluble.com/92/8a/73/928a730ca6c2029d5a531dee6ec1efdf.js"

# دالة حفظ المشتركين في قاعدة البيانات
def save_user(user_id):
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: pass
    with open(DB_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(DB_FILE, "a") as f:
            f.write(str(user_id) + "\n")

# أمر البداية مع جميع الميزات والأقسام
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    
    # أزرار الخدمات والألعاب والهدايا (تفتح روابطك)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btns = [
        types.InlineKeyboardButton("🎡 عجلة الحظ", url=LINK_1),
        types.InlineKeyboardButton("🔑 إدخال كود الهدية", url=LINK_2),
        types.InlineKeyboardButton("🎯 مهام سريعة", url=LINK_1),
        types.InlineKeyboardButton("🏆 قائمة المتصدرين", url=LINK_2),
        types.InlineKeyboardButton("🔫 شحن شدات ببجي", url=LINK_1),
        types.InlineKeyboardButton("💎 جواهر فري فاير", url=LINK_2),
        types.InlineKeyboardButton("🎁 صندوق عشوائي", url=LINK_1),
        types.InlineKeyboardButton("💳 بطاقات جوجل", url=LINK_2),
        types.InlineKeyboardButton("⚡ ربح نقاط سريع", url=LINK_1),
        types.InlineKeyboardButton("📲 تطبيقات مدفوعة", url=LINK_2)
    ]
    markup.add(*btns)
    
    # القائمة السفلية للتحكم بالبوت
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

# ميزة الإذاعة للآدمن (بإرسال /send)
@bot.message_handler(commands=['send'])
def broadcast_command(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "اكتب الرسالة (نص أو رابط) التي تريد توزيعها على الجميع:")
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
            continue # تخطي المستخدمين الذين حظروا البوت
            
    bot.send_message(ADMIN_ID, f"✅ تمت الإذاعة بنجاح!\nتم الإرسال إلى {count} مشترك.")

# تشغيل السيرفر والبوت معاً
if __name__ == "__main__":
    # تشغيل Flask في خيط مستقل
    t = Thread(target=run_flask)
    t.start()
    # تشغيل البوت للأبد
    print("Bot is started successfully...")
    bot.infinity_polling()
