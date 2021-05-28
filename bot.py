import requests
import telebot
from telebot import types
import config as config

bot = telebot.TeleBot(config.token)

# /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, text='Hi! Im a bot who can show you where to rest, and where to stay⤵️'
                                           '\ntype /help')


# /help
@bot.message_handler(commands=['help'])
def handle_help(message):
        key_add = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(text='🌍Give me a random place🌍', callback_data='key1')
        key_add.add(key1)
        key2 = types.InlineKeyboardButton(text='🏨Show me a hotel🏨', callback_data='key2')
        key_add.add(key2)
        key3 = types.InlineKeyboardButton(text='🤡Give me a joke🤡', callback_data='key3')
        key_add.add(key3)
        bot.send_message(message.from_user.id, text='How can I help you? ⤵', reply_markup=key_add)

# Натиск на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
        # Якщо натиснули на одну з кнопок
        if call.data == "key1":
            req = requests.request("GET", url=config.place_api)
            response = req.json()
            country_name = response['data']['AR']['name']
            country_continent = response['data']['AR']['continent']
            country_score = response['data']['AR']['advisory']['score']
            country_message = response['data']['AR']['advisory']['message']
            bot.send_message(call.message.chat.id, f"⏹ Name: {country_name}🇦🇷"
                                                   f"\n⏹ Continent: {country_continent}"
                                                   f"\n↗️ Score: {country_score}"
                                                   f"\n\n⏹ {country_message}")

        if call.data == "key2":

            headers = {
                'x-rapidapi-key': "a7544b7cd9msh560c79499597685p1cdb49jsn63c7b4d689e5",
                'x-rapidapi-host': "hotels4.p.rapidapi.com"
            }
            requ = requests.request("GET", url=config.hotel_api, headers=headers)

            response1 = requ.json()
            name = response1[0]['name']
            posname = response1[0]['posName']
            bot.send_message(call.message.chat.id, f"🏨Name: {name}🏨"
                                                   f"\n\n🏨PosName: {posname}🏨")

        if call.data == "key3":
            req = requests.get(config.joke_api)  # Link з API
            response = req.json()  # Список у форматі JSON
            tell_joke = response["joke"]  # Витягуєм жарт з JSON
            bot.send_message(call.message.chat.id,f"😜{tell_joke}😜")


# Запускаємо постійне опитування бота в Телеграм
bot.polling(none_stop=True, interval=0)


