import telebot
from config import *
from extensions import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Привет 👋 \nЧтобы начать работу введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nЧтобы увидить все доступные валюты, нажми: /values. \nЧтобы выйти, нажми: /exit'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации:'
    for i in currencies.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['yes'])
def start(message: telebot.types.Message):
    text = 'Введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>. \nЧтобы увидить все доступные валюты, нажми: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['exit'])
def start(message: telebot.types.Message):
    text = 'До встречи 👋'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) > 3:
            raise APIException('Слишком много параметров. \nПовторить попытку? /yes')
        if len(values) < 3:
            raise APIException('Слишком мало параметров. \nПовторить попытку? /yes')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'⛔ Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} - {total_base} {base} \nПовторим конвертацию? /yes\nДля выхода нажми: /exit'
        bot.send_message(message.chat.id, text)


bot.polling()
