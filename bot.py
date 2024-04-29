import telebot
from telebot import types


def bot_main(context):
    bot = telebot.TeleBot(context['token'])
    markup_start = types.ReplyKeyboardMarkup()
    markup_start.add(types.KeyboardButton('Перейти к оплате'))
    markup_start.add(types.KeyboardButton('Подробнее про курс'))

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "Привет, это наш бот(текст 1)", reply_markup=markup_start)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        if message.text == 'Перейти к оплате':
            bot.send_invoice(
                chat_id=message.chat.id,
                title="Доступ к курсу(текст 4)",
                description="описание(текст 5)",
                invoice_payload="your_payload",
                currency='RUB',
                provider_token=context['pay_token'],
                start_parameter="test",
                prices=[types.LabeledPrice(label='Курс', amount=10000)]
            )
        elif message.text == 'Подробнее про курс':
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Программа курса'))
            markup.add(types.KeyboardButton('Как проходят занятия?'))
            bot.reply_to(message, "Полотно про курс", reply_markup=markup)

        elif message.text == 'Как проходят занятия?':
            bot.reply_to(message, "Полотно про орг моменты", reply_markup=markup_start)

        elif message.text == 'Программа курса':
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Ок, а что дальше?'))
            bot.reply_to(message, "Полотно первое занятие", reply_markup=markup)

        elif message.text == 'Ок, а что дальше?':
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Хорошо, что дальше?'))
            bot.reply_to(message, "Полотно второе занятие", reply_markup=markup)

        elif message.text == 'Хорошо, что дальше?':
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('А что дальше?'))
            bot.reply_to(message, "Полотно третье занятие", reply_markup=markup)

        elif message.text == 'А что дальше?':
            bot.reply_to(message, "Полотно четвертое занятие", reply_markup=markup_start)

    @bot.pre_checkout_query_handler(func=lambda query: True)
    def checkout(pre_checkout_query):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Ошибка, свяжитесь с @aluv2036")

    @bot.message_handler(content_types=['successful_payment'])
    def got_payment(message):
        url = bot.create_chat_invite_link(chat_id=context['chanel_id'], member_limit=1).invite_link
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton(text='Перейти в канал', url=url))
        bot.send_message(context['log_chat_id'], f'{message.from_user.id}, {message.from_user.first_name} {message.from_user.last_name}, @{message.from_user.username} купил курс')
        bot.send_message(message.chat.id, 'Вы оплатили курс(текст 8)', reply_markup=markup)

    bot.polling(non_stop=True, interval=0)
