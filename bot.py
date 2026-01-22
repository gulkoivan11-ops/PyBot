import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import requests
import os
from flask import Flask, request

token = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(token)
lastjoke = ''

jokes = [
    'Дружина посилає чоловіка-програміста в магазин:\n— Купи батон. А якщо будуть яйця — візьми десяток.\nПрограміст повертається додому з десятьма батонами.\nДружина в шоці:\n— Навіщо ти купив стільки хліба?!\n— Ну так яйця ж були!',
    'Їдуть в машині інженер-механік та програміст. Раптом двигун глухне, машина зупиняється.\nМеханік:\n— Так, треба перевірити свічки, потім карбюратор, подивитися подачу палива...\nПрограміст:\n— А може, просто вийдемо і зайдемо знову?',
    'У світі існує 10 типів людей: ті, хто розуміє двійкову систему числення, і ті, хто ні.',
    '99 помилок у коді, 99 помилок.\nОдну виправив, закоммітив...\n127 помилок у коді!',
    '— Скільки програмістів потрібно, щоб змінити лампочку?\n— Жодного. Це апаратна проблема (hardware problem).',
    'Заходить SQL-запит у бар, бачить два столики і каже:\n— Можна до вас приєднатися? (Can I JOIN you?)',
    'Програміст просить у колеги в борг:\n— Позич 1000 гривень до зарплати.\n— Та тримай.\n— Слухай, а дай краще 1024, щоб рівне число було!',
    'Програміст перед сном ставить на тумбочку дві склянки. Одну з водою — на випадок, якщо захоче пити. Другу порожню — на випадок, якщо не захоче.',
    'Стакан наполовину повний — каже оптиміст.\nСтакан наполовину порожній — каже песиміст.\nСтакан у 2 рази більший, ніж необхідно — каже програміст.',
    'Як на цілий день зайняти програміста в душі?\nДати йому шампунь, на якому написано: "Намилити, змити, повторити".',
    'Заходить тестувальник у бар. Замовляє:\n— кухоль пива,\n— 2 кухлі пива,\n— 0 кухлів пива,\n— 999999999 кухлів пива,\n— ящірку,\n— -1 кухоль пива.\nЗамовлення прийнято. Заходить реальний клієнт, питає "Де туалет?" — і бар згоряє.',
    'Чому програмісти люблять темну тему оформлення?\nТому що світло приваблює багів (bugs).',
    'Бог створив світ за 6 днів.\nА все чому? У нього просто не було легасі-коду і вимог щодо сумісності з попередніми версіями.',
    'Джуніор: «Я написав код, і він працює, але я не знаю чому».\nСеньйор: «Я написав код, він не працює, і я теж не знаю чому».',
    'Код — як жарт. Якщо його доводиться пояснювати (коментарями), то він поганий.',
    '— У чому різниця між "залізом" (hardware) і "софтом" (software)?\n— "Залізо" — це те, що можна вдарити ногою, коли воно не працює. А "софт" — це те, що можна лише обматюкати.',
    'Тімлід: «Скільки часу займе ця задача?»\nПрограміст: «Ну, годинки дві...»\n(Голос за кадром: «Минув третій тиждень...»)',
    'Програмування на 10% складається з написання коду і на 90% з гугління помилок.',
    'Найстрашніший сон програміста: ти помер, потрапив у пекло, а чорти змушують тебе підтримувати твій власний код, написаний 5 років тому без коментарів.',
    'Зустрічаються два програмісти:\n— Ну як, ти вже закрив той баг?\n— Ні, ми з ним ще не домовилися.'
]

def get_exchange_rates():
    usd = 43.0
    eur = 50.5
    try:
        response = requests.get('https://api.monobank.ua/bank/currency', timeout=5)
        data = response.json()
        for item in data:
            if item.get('currencyCodeA') == 840 and item.get('currencyCodeB') == 980:
                usd = round((float(item['rateBuy']) + float(item['rateSell'])) / 2, 2)
            elif item.get('currencyCodeA') == 978 and item.get('currencyCodeB') == 980:
                eur = round((float(item['rateBuy']) + float(item['rateSell'])) / 2, 2)
    except Exception:
        pass
    return usd, eur

usdrate, eurrate = get_exchange_rates()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Інформація", callback_data='1'),
        InlineKeyboardButton("Почати", callback_data='2')
    )
    bot.send_message(message.chat.id, "Привіт! Обери дію:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    bot.answer_callback_query(call.id)

    if call.data == "1":
        bot.send_message(call.message.chat.id, "Я - бот, що допомагає в житті та вміє жартувати!")

    elif call.data == "2":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("Роскажи жарт", callback_data='3'),
            InlineKeyboardButton("Пограти в камінь-ножиці-бумага", callback_data='4'),
            InlineKeyboardButton("Конвертор валют", callback_data='5')
        )
        bot.send_message(call.message.chat.id, "Давай почнемо! Що саме тебе цікавить?", reply_markup=keyboard)

    elif call.data == "3":
        global lastjoke
        joke = random.choice([j for j in jokes if j != lastjoke])
        lastjoke = joke
        bot.send_message(call.message.chat.id, joke)

    elif call.data == "4":
        game = InlineKeyboardMarkup()
        game.add(
            InlineKeyboardButton("Камінь", callback_data='rock'),
            InlineKeyboardButton("Ножиці", callback_data='scissors'),
            InlineKeyboardButton("Папір", callback_data='paper')
        )
        bot.send_message(call.message.chat.id, "Вибери свій хід:", reply_markup=game)

    elif call.data in ['rock', 'scissors', 'paper']:
        bot_choice = random.choice(['rock', 'scissors', 'paper'])
        if call.data == bot_choice:
            result = "Нічия!"
        elif (call.data == 'rock' and bot_choice == 'scissors') or \
             (call.data == 'scissors' and bot_choice == 'paper') or \
             (call.data == 'paper' and bot_choice == 'rock'):
            result = "Ти виграв!"
        else:
            result = "Бот виграв!"
        again = InlineKeyboardMarkup()
        again.add(
            InlineKeyboardButton("Так!", callback_data='4'),
            InlineKeyboardButton("Ні", callback_data='no')
        )
        bot.send_message(call.message.chat.id, result + "\nХочеш зіграти ще раз?", reply_markup=again)

    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Ок, повертайся, коли захочеш!")

    elif call.data == "5":
        exchange = InlineKeyboardMarkup()
        exchange.add(
            InlineKeyboardButton("USD → UAH", callback_data='usduan'),
            InlineKeyboardButton("EUR → UAH", callback_data='euruan'),
            InlineKeyboardButton("UAH → USD", callback_data='uanusd'),
            InlineKeyboardButton("UAH → EUR", callback_data='uaneur')
        )
        bot.send_message(call.message.chat.id, "Вибери напрямок обміну:", reply_markup=exchange)

    elif call.data in ['usduan', 'euruan', 'uanusd', 'uaneur']:
        msg = bot.send_message(call.message.chat.id, "Введіть суму для конвертації (тільки число):")
        bot.register_next_step_handler(msg, process_conversion, call.data)

def process_conversion(message, conversion_type):
    try:
        amount = float(message.text)
        if conversion_type == 'usduan':
            result = amount * usdrate
            currency = "UAH"
        elif conversion_type == 'euruan':
            result = amount * eurrate
            currency = "UAH"
        elif conversion_type == 'uanusd':
            result = amount / usdrate
            currency = "USD"
        else:
            result = amount / eurrate
            currency = "EUR"
        bot.send_message(message.chat.id, f"Результат: {round(result, 2)} {currency}")
    except ValueError:
        bot.send_message(message.chat.id, "Помилка! Потрібно ввести число.")

app = Flask(__name__)

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def health():
    return "ok"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(os.environ["RENDER_EXTERNAL_URL"] + "/telegram")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
