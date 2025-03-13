from bot import bot_main
context = {
    'token': 'API_TOKEN',
    'chanel_id': '-1002023642883',
    'log_chat_id': '-1002026292785',
    'pay_token': "PAY_TOKEN",
    'courses': ['Моделлинг', 'Композиция и освещение', 'Материалы', 'Финализация'],
    'link_temp_chat': 'https://t.me/+IjIBC8vlxrRlNDgy'

}
while True:
    try:
        bot_main(context)
    except Exception as e:
        bot_main(context)
        print(e)
