import telebot
from telebot import types
from functions import *


def bot_main(context):
    bot = telebot.TeleBot(context.token)
    temp_list = []
    markup_start = types.ReplyKeyboardMarkup()
    markup_start.add(types.KeyboardButton('Подробнее про курс'))
    markup_start.add(types.KeyboardButton('Как проходят занятия?'))
    markup_start.add(types.KeyboardButton('Программа курса'))
    markup_start.add(types.KeyboardButton('Записаться на курс'))

    @bot.message_handler(commands=['start'])
    def start(message):
        text_path = f'data/texts/about/hello.txt'

        send_text_message(text_path, message, markup_start, bot)

    @bot.message_handler(content_types=['text'])
    def text_handler(message):
        if message.text == 'Записаться на курс':
            text_path = f'data/texts/about/price.txt'
            photo_path = f'data/photos/about/оплата_занятий.jpg'

            markup = types.ReplyKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Записаться'))
            markup.add(types.InlineKeyboardButton('Не могу оплатить всю сумму сразу'))

            send_photo_message(text_path, photo_path, message, markup, bot)
        elif message.text == 'Записаться':
            temp_list.append(message.from_user.id)
            temp_list.append(message.from_user.id)

            text_path = f'data/texts/about/price_names.txt'
            send_text_message(text_path, message, types.ReplyKeyboardRemove(), bot)

        elif message.text == 'Не могу оплатить всю сумму сразу':
            markup = types.InlineKeyboardMarkup()
            markup.row(types.InlineKeyboardButton(text='Перейти в чат поддержки', url=context.link_temp_chat))
            bot.send_message(message.chat.id, 'Пишите, постараемся найти компромисс')
            bot.register_next_step_handler(message, start)

        elif message.text == 'Подробнее про курс':

            text_path = f'data/texts/about/about_all.txt'
            photo_path = f'data/photos/about/как_устроен_курс.jpg'

            send_photo_message(text_path, photo_path, message, markup_start, bot)

        elif message.text == 'Как проходят занятия?':
            text_path = f'data/texts/about/about_lessons.txt'
            photo_path = f'data/photos/about/как_проходят_занятия.jpg'

            send_photo_message(text_path, photo_path, message, markup_start, bot)

        elif message.text == 'Программа курса':
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Хочу больше узнать о каждом блоке'))
            markup.add(types.KeyboardButton('Темы лекций'))
            markup.add(types.KeyboardButton('Записаться на курс'))

            text_path = f'data/texts/about/course_program.txt'
            photo_path = f'data/photos/about/программа_курса.jpg'

            send_photo_message(text_path, photo_path, message, markup, bot)

        elif message.text == 'Темы лекций':
            markup = markup_start
            markup.add(types.KeyboardButton('Программа курса'))

            text_path = f'data/texts/about/about_lectures.txt'
            photo_path = f'data/photos/about/темы_лекций.jpg'

            send_photo_message(text_path, photo_path, message, markup, bot)

        elif message.text == 'Хочу больше узнать о каждом блоке':
            markup = types.ReplyKeyboardMarkup()
            for i in context.courses:
                markup.add(types.KeyboardButton(i))

            bot.reply_to(message, "Выберите раздел, который вас интересует.", reply_markup=markup)

        elif message.text in context.courses:
            markup = types.ReplyKeyboardMarkup()
            for i in context.courses:
                markup.add(types.KeyboardButton(i))
            markup.add(types.KeyboardButton('Записаться на курс'))

            course_number = context.courses.index(message.text) + 1

            text_path = f'data/texts/courses/course_{course_number}.txt'
            photo_path = f'data/photos/courses/{course_number}.jpg'

            send_photo_message(text_path, photo_path, message, markup, bot)

        elif message.from_user.id in temp_list:
            if temp_list.count(message.from_user.id) == 2:
                temp_list.remove(message.from_user.id)
                bot.send_message(context.log_chat_id, message.text)
                bot.send_message(message.chat.id, 'В какие дни и в какое время вам удобнее всего ходить на занятия?')

            elif temp_list.count(message.from_user.id) == 1:
                temp_list.remove(message.from_user.id)
                bot.send_message(context.log_chat_id, message.text)
                if context.payment_ready:
                    '''
                                bot.send_invoice(
                                    chat_id=message.chat.id,
                                    title="Доступ к курсу(текст 4)",
                                    description="описание(текст 5)",
                                    invoice_payload="your_payload",
                                    currency='RUB',
                                    provider_token=context.pay_token,
                                    start_parameter="test",
                                    prices=[types.LabeledPrice(label='Курс', amount=10000)]
                                )'''
                    print('sdsds')
                else:
                    markup = types.InlineKeyboardMarkup()
                    markup.row(types.InlineKeyboardButton(text='Перейти в чат участников', url=context.link_temp_chat))
                    markup.row(types.InlineKeyboardButton(text='Перейти в чат поддержки', url=context.link_temp_chat))

                    text_path = f'data/texts/about/after_price_false'

                    send_text_message(text_path, message, markup, bot)

                    bot.register_next_step_handler(message, start)

    @bot.pre_checkout_query_handler(func=lambda query: True)
    def checkout(pre_checkout_query):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Ошибка, свяжитесь с @aluv2036")

    @bot.message_handler(content_types=['successful_payment'])
    def got_payment(message):
        url = bot.create_chat_invite_link(chat_id=context.chanel_id, member_limit=1).invite_link

        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton(text='Перейти в канал', url=url))

        bot.send_message(context.log_chat_id, f'{message.from_user.id}, {message.from_user.first_name} {message.from_user.last_name}, @{message.from_user.username} купил курс')
        bot.send_message(message.chat.id, 'Вы оплатили курс(текст 8)', reply_markup=markup)

    bot.polling(non_stop=True, interval=0)
