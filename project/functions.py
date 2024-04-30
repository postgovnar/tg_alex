import time

def send_text_message(text_path, message, markup, bot):
    with open(text_path, 'r', encoding="utf-8") as f:
        text = ''.join(f.readlines())
    bot.reply_to(message, text, reply_markup=markup, parse_mode="Markdown")


def send_photo_message(text_path, photo_path, message, markup, bot, flag=False, photo_id=None):
    if flag:
        print(photo_id)
    else:
        with open(text_path, 'r', encoding="utf-8") as f:
            text = ''.join(f.readlines())
        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup, caption=text, parse_mode="Markdown")


def log(message, text=''):
    with open('../data/users/log.txt', 'a') as f:
        tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

        f.write(f'{tconv(message.date)}; {message.from_user.id}; @{message.from_user.username}; {text}')

