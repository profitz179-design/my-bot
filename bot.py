import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Application, CommandHandler,
                           MessageHandler, filters,
                           ContextTypes, ConversationHandler)
from sheet import save_client

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

NAME, PHONE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً! للتسجيل أحتاج منك معلومتين بس.\n\nما اسمك الكريم؟"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    button = KeyboardButton("📱 مشاركة رقمي", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "ممتاز! الآن اضغط الزر لمشاركة رقم هاتفك 👇",
        reply_markup=keyboard
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text

    name = context.user_data["name"]
    chat_id = update.message.chat_id

    save_client(name, phone, chat_id)

    invite_link = await context.bot.create_chat_invite_link(
        chat_id=int(GROUP_ID),
        member_limit=1
    )

    await update.message.reply_text(
        f"✅ تم تسجيلك بنجاح يا {name}!\n\n"
        f"اضغط هنا للدخول للمجموعة 👇\n{invite_link.invite_link}"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء. اكتب /start للبدء من جديد.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [
                MessageHandler(filters.CONTACT, get_phone),
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)
    print("البوت شغال ✅")
    app.run_polling()

if __name__ == "__main__":
    main()