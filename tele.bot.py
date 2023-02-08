import telebot
import requests
import random

bot = telebot.TeleBot(
    "ТОКЕН", parse_mode=None)
game_start = False
random_number = None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Привет, {message.from_user.first_name}?")


@bot.message_handler(content_types=['text'])
def echo_all(message):
    global game_start
    global random_number
    if game_start:
        if message.text.isdigit():
            sum_numb = 0
            user_number = int(message.text)
            if user_number > random_number:
                bot.reply_to(
                    message, f"{message.from_user.first_name}, мое число меньше.")
            elif user_number < random_number:
                bot.reply_to(
                    message, f"{message.from_user.first_name}, мое число больше.")
            elif user_number == random_number:
                game_start = False
                bot.reply_to(
                    message, f"{message.from_user.first_name}, ты угадал. Я загадал число {random_number}.")
            else:
                bot.reply_to(
                    message, f"{message.from_user.first_name}, ничего не понял.")
        else:
            bot.reply_to(
                message, f"{message.from_user.first_name}, я жду число.")

    if message.text == 'Погода':
        data = requests.get('https://wttr.in/?format=4')
        bot.reply_to(message, data.text)
    elif message.text == 'Собака':
        dog = open('dog.jpeg', 'rb')
        bot.send_photo(message.from_user.id, dog)
    elif message.text == 'Играть':
        if not game_start:
            game_start = True
            random_number = random.randint(1, 10)
            bot.reply_to(
                message, f"{message.from_user.first_name}, я загадал число от 1 до 1000. Попробуй его угадать")
        else:
            bot.reply_to(
                message, f"{message.from_user.first_name}, ты уже играешь.")
    elif message.text == 'Вычесли':
        bot.reply_to(message, "Введи выражение")
        bot.register_next_step_handler(message, calculate)


def calculate(message):
    try:
        bot.reply_to(message, f" ответ: {eval(message.text)}")
    except NameError:
        bot.reply_to(message, "Вы ввели не верное выражение")


bot.infinity_polling()
