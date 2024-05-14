from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
from datetime import datetime

# Встановлення параметрів бота
TELEGRAM_TOKEN = '5874335640:AAEmriZ0z1gS70_NRXVEmOPwn_U_S-zaxEk'  # Ваш токен бота
GROUP_CHAT_ID = '-1001945580350'  # ID вашої групи в Telegram

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція, що відправляє повідомлення з кнопками
async def send_request_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Додавання прикладу даних, які могли бути отримані з вебсайту
    request_data = "Нова заявка: Ім'я - Олексій, Телефон - 0987654321"
    keyboard = [
        [InlineKeyboardButton("Взяти в обробку", callback_data='take')],
        [InlineKeyboardButton("Оброблено", callback_data='done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=request_data, reply_markup=reply_markup)

# Функція для обробки натискання кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user = query.from_user
    if query.data == 'take':
        taken_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await context.bot.send_message(chat_id=GROUP_CHAT_ID,
                                       text=f"Взято в обробку користувачем {user.first_name} {user.last_name} о {taken_time}")
    elif query.data == 'done':
        done_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await context.bot.send_message(chat_id=GROUP_CHAT_ID,
                                       text=f"Заявку успішно оброблено {user.first_name} {user.last_name} о {done_time}")

# Головна функція, яка ініціалізує бота
def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # Додавання обробника команд для демонстрації
    application.add_handler(CommandHandler('send_request', send_request_to_group))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == '__main__':
    main()
