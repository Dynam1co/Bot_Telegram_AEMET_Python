from telegram.ext import Updater
from telegram.ext import CommandHandler
import aemet
import conf_management as ConfMgt
import schedule
import time


def start(bot, update):
    message = "Bienvenido al bot de AEMET!"
    bot.send_message(chat_id=update.message.chat_id, text=message)


def weather(bot, update):
    ok = False
    result_text = ''

    ok, result_text = aemet.get_weather(ConfMgt.get_aemet_token())

    if not ok:
        bot.send_message(chat_id=update.message.chat_id, text='Error al conectar con AEMET')
    else:
        bot.send_message(chat_id=update.message.chat_id, text=result_text)


def main(bot_token):
    """ Main function of the bot """
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Command handlers
    start_handler = CommandHandler('start', start)
    weather_handler = CommandHandler('weather', weather)

    # Add the handlers to the bot
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(weather_handler)

    # Starting the bot
    updater.start_polling()


def envia_telegram(bot_token, id_chat, texto_enviar):
    update = Updater(token=bot_token)
    update.bot.send_message(chat_id=id_chat, text=texto_enviar)


def check_weather():
    ok = False
    result_text = ''

    ok, result_text = aemet.get_weather(ConfMgt.get_aemet_token())

    if not ok:
        envia_telegram(ConfMgt.get_telegram_token(), ConfMgt.get_telegram_group_id(), 'Error al conectar con AEMET')
    else:
        envia_telegram(ConfMgt.get_telegram_token(), ConfMgt.get_telegram_group_id(), result_text)


if __name__ == "__main__":
    main(ConfMgt.get_telegram_token())

    for hour in ConfMgt.get_schedule():
        schedule.every().day.at(hour).do(check_weather)

    while True:
        schedule.run_pending()
        time.sleep(1)
