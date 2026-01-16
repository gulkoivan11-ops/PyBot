import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import requests
import os
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
                buy = float(item.get('rateBuy'))
                sell = float(item.get('rateSell'))
                usd = round((buy + sell)/2, 2)
            elif item.get('currencyCodeA') == 978 and item.get('currencyCodeB') == 980:
                buy = float(item.get('rateBuy'))
                sell = float(item.get('rateSell'))
                eur = round((buy + sell)/2, 2)
    except Exception as e:
        print(f"Помилка отримання курсів: {e}")
    return usd, eur
usdrate, eurrate = get_exchange_rates()
print(f"Курс завантажено: USD={usdrate}, EUR={eurrate}")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Інформація", callback_data='1')
    button2 = InlineKeyboardButton("Почати", callback_data='2')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Привіт! Обери дію:", reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(call):
    bot.answer_callback_query(call.id)
    if call.data == "1":
        bot.send_message(call.message.chat.id, "Я - бот, що допомагає в житті та вміє жартувати!")
    elif call.data == "2":
        keyboard1 = InlineKeyboardMarkup()
        but1 = InlineKeyboardButton("Роскажи жарт", callback_data='3')
        but2 = InlineKeyboardButton("Пограти в камінь-ножиці-бумага", callback_data='4')
        but3 = InlineKeyboardButton("Конвертор валют", callback_data='5')
        keyboard1.add(but1)
        keyboard1.add(but2)
        keyboard1.add(but3)
        bot.send_message(call.message.chat.id, "Давай почнемо! Що саме тебе цікавить?", reply_markup=keyboard1)
    elif call.data == "3":
        global lastjoke
        while True:
            joke = random.choice(jokes)
            if joke == lastjoke:
                continue
            else:
                bot.send_message(call.message.chat.id, text=joke)
                lastjoke = joke
                break
    elif call.data == "4":
        game = InlineKeyboardMarkup()
        gamebut1 = InlineKeyboardButton("Камінь", callback_data='rock')
        gamebut2 = InlineKeyboardButton("Ножиці", callback_data='scissors')
        gamebut3 = InlineKeyboardButton("Папір", callback_data='paper')
        game.add(gamebut1, gamebut2, gamebut3)
        bot.send_message(call.message.chat.id, "Вибери свій хід:", reply_markup=game)
    elif call.data in ['rock', 'scissors', 'paper']:
        user_choice = call.data
        bot_choice = random.choice(['rock', 'scissors', 'paper'])
        if user_choice == bot_choice:
            result_text = "Нічия!"
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
                (user_choice == 'scissors' and bot_choice == 'paper') or \
                (user_choice == 'paper' and bot_choice == 'rock'):
            result_text = "Ти виграв!"
        else:
            result_text = "Бот виграв!"
        again = InlineKeyboardMarkup()
        againyes = InlineKeyboardButton("Так!", callback_data='4')
        againno = InlineKeyboardButton("Ні", callback_data='no')
        again.add(againyes, againno)
        bot.send_message(call.message.chat.id, result_text + "\nХочеш зіграти ще раз?", reply_markup=again)

    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Ок, повертайся, коли захочеш!")

    elif call.data == '5':
        exchange = InlineKeyboardMarkup()
        usduan = InlineKeyboardButton("USD → UAH", callback_data='usduan')
        euruan = InlineKeyboardButton("EUR → UAH", callback_data='euruan')
        uanusd = InlineKeyboardButton("UAH → USD", callback_data='uanusd')
        uaneur = InlineKeyboardButton("UAH → EUR", callback_data='uaneur')
        exchange.add(usduan, euruan)
        exchange.add(uanusd, uaneur)
        bot.send_message(call.message.chat.id, "Вибери напрямок обміну:", reply_markup=exchange)

    elif call.data in ['usduan', 'euruan', 'uanusd', 'uaneur']:
        msg = bot.send_message(call.message.chat.id, "Введіть суму для конвертації (тільки число):")
        bot.register_next_step_handler(msg, process_conversion, call.data)
    else:
        bot.send_message(call.message.chat.id, "Невідома команда")

def process_conversion(message, conversion_type):
    try:
        amount = float(message.text)
        result = 0
        if conversion_type == 'usduan':
            result = amount * usdrate
            currency_symbol = "UAH"
        elif conversion_type == 'euruan':
            result = amount * eurrate
            currency_symbol = "UAH"
        elif conversion_type == 'uanusd':
            result = amount / usdrate
            currency_symbol = "USD"
        elif conversion_type == 'uaneur':
            result = amount / eurrate
            currency_symbol = "EUR"
        result = round(result, 2)
        bot.send_message(message.chat.id, f"Результат: {result} {currency_symbol}")

    except ValueError:
        bot.send_message(message.chat.id,"Помилка! Потрібно ввести число. Спробуй ще раз, натиснувши кнопку.")

bot.infinity_polling()