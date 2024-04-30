from bot import bot_main
from config import config as context
try:
    bot_main(context)
except Exception as e:
    print(e)
