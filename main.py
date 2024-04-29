from bot import bot_main
context = {
    'token': '6749400221:AAGdCxorRoZSqnI0eJiUcuhlQXb_39cEF14',
    'chanel_id': '-1002023642883',
    'log_chat_id': '-1002026292785',
    'pay_token': "381764678:TEST:83859"
}
while True:
    try:
        bot_main(context)
    except Exception as e:
        bot_main(context)
        print(e)
