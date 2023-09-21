import telebot
import random
import time
import threading

# Импортируем необходимые классы и модули для работы с Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Устанавливаем токен бота и создаем объект бота
bot_token = '000000000000000000'
bot = telebot.TeleBot(bot_token)

# Устанавливаем доступ к Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('0000000000.json', scope)
client = gspread.authorize(creds)

# Открываем таблицу "users"
users_sheet = client.open('Ramesh-VIP-Bot').worksheet('users')

# Словарь для отслеживания пользователей и их состояний
user_data = {}

# Функция для отправки сигнала пользователю
def send_signal_message(user_id):
    # Проверяем, был ли пользователь уже зарегистрирован
    if user_id not in user_data:
        user_data[user_id] = {
            'registered': False,
            'last_received_signal_time': 0,
            'signal_count': 0
        }
    current_time = time.time()
    last_received_signal_time = user_data[user_id]['last_received_signal_time']

    # Проверяем ограничение на частоту запросов сигнала
    if current_time - last_received_signal_time < 90:
        remaining_time = int(90 - (current_time - last_received_signal_time))
        bot.send_message(user_id, f"😴Wait {remaining_time} seconds to receive the next signal.😴")
        return

    user_data[user_id]['last_received_signal_time'] = current_time
    user_data[user_id]['signal_count'] += 1

    # Генерируем случайные числа
    lower_limit = round(random.uniform(1.3, 5.4), 1)
    recommended_stake = random.randrange(300, 1501, 20)
    message = f"Bet on {lower_limit}x ✅\n<strong>Amount from: {recommended_stake} INR</strong>"

    # Вероятность выпадения случайных чисел от 5.5 до 7.0 примерно 10%
    if random.random() < 0.1:
        random_number = round(random.uniform(5.5, 7.0), 1)
        message = f"\nDon't miss the next signal {random_number}x ✅!!\n<strong>Amount from: {recommended_stake} INR</strong>"

    # Отправляем сообщение пользователю
    bot.send_message(user_id, 'The bot calculated a new coefficient...⏳')
    time.sleep(3)
    bot.send_message(user_id, message, parse_mode='HTML')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    users_sheet.append_row([username, user_id])
    bot.send_message(user_id, f"Welcome, {username}. This artificial intelligence based bot makes game calculations with 96% accuracy. Just follow the bot's instructions and ensure a rich life for yourself.", parse_mode='HTML')
    send_keyboard(user_id)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    send_keyboard(user_id)

# Функция для отправки клавиатуры с кнопками "Support" и "Receive Signal"
def send_keyboard(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_receive_signal = telebot.types.KeyboardButton("Receive Signal💸")
    item_support = telebot.types.KeyboardButton("Support🦸")
    markup.row(item_receive_signal)
    markup.row(item_support)
    bot.send_message(user_id, "Choose an action:👇", reply_markup=markup)

# Функция Support
def get_support_button():
    markup = telebot.types.InlineKeyboardMarkup()
    item_support = telebot.types.InlineKeyboardButton(text="Contact support🦸", url="https://google.com")
    markup.add(item_support)
    return markup

# Обработчик текстовых сообщений от пользователя
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    text = message.text

    if text == "Receive Signal💸":
        send_signal_message(user_id)

    elif text == "Support🦸":
        # Здесь вы можете реализовать перенаправление на службу поддержки или другие действия
        bot.send_message(user_id, text="🦸Our 24/7 support will help you with any questions you may have!", reply_markup=get_support_button())


# Запускаем бота
bot.polling(none_stop=True)
