import telebot
from telebot import types

# 1. إعدادات البوت (التوكن الخاص بك)
API_TOKEN = '8788993987:AAGNz5XTpcA14szp7b-hFlueFFUIzuPyd88'
bot = telebot.TeleBot(API_TOKEN)

# 2. الروابط الجديدة (الرابطين اللي طلبتهم + رابط الإحالة)
SMART_LINK_1 = "https://encyclopediainsoluble.com/zkwsxfxbs7?key=7ea007649e568f3e7a8150dc4bb54f02"
SMART_LINK_2 = "https://encyclopediainsoluble.com/92/8a/73/928a730ca6c2029d5a531dee6ec1efdf.js"
REFERRAL_LINK = "Https://beta.publishers.adsterra.com/referral/xt8ah9W31d"

@bot.message_handler(commands=['start'])
def start(message):
    # أزرار الشاشة (Inline)
    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    
    # توزيع الروابط على أزرار الألعاب والكسب
    btn1 = types.InlineKeyboardButton("💰 ابدأ كسب النقاط الآن", url=SMART_LINK_1)
    btn2 = types.InlineKeyboardButton("🎮 قسم ألعاب ومسابقات", url=SMART_LINK_2)
    btn_ref = types.InlineKeyboardButton("👥 دعوة صديق (اربح 1$)", url=REFERRAL_LINK)
    
    inline_markup.add(btn1, btn2, btn_ref)

    # أزرار التحكم بالأسفل (Reply Keyboard)
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(types.KeyboardButton('🏠 القائمة الرئيسية'))
    reply_markup.add(types.KeyboardButton('👤 حسابي'), types.KeyboardButton('💰 رصيدي'))

    welcome_text = (
        f"أهلاً بك {message.from_user.first_name} في بوت الجوائز! 🏆\n\n"
        "تم تحديث النظام! يمكنك الآن جمع النقاط من خلال الأزرار أدناه.\n"
        "ادخل إلى قسم الألعاب أو ابدأ الكسب المباشر فوراً."
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=inline_markup)
    bot.send_message(message.chat.id, "استخدم الأزرار بالأسفل لإدارة حسابك 👇", reply_markup=reply_markup)

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == '🏠 القائمة الرئيسية':
        start(message)
    elif message.text == '👤 حسابي':
        text = (f"👤 **معلومات الحساب:**\n\n"
                f"• الاسم: {message.from_user.first_name}\n"
                f"• المعرف: `{message.from_user.id}`\n"
                f"• الحالة: نشط ✅")
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    elif message.text == '💰 رصيدي':
        text = ("💰 **تفاصيل الرصيد:**\n\n"
                "• النقاط: 0\n"
                "• الأرباح المتاحة: 0.00$\n\n"
                "أكمل المهام من الروابط بالأعلى لزيادة رصيدك.")
        bot.send_message(message.chat.id, text, parse_mode="Markdown")

print("البوت يعمل الآن مع قسم الألعاب والروابط الجديدة...")
bot.polling()
