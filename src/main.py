import telebot
from src.actions.actions import actionsInit
from src.answer.botActions import BotActions
from src.answer.answer import ANSWER_BOT
from src.db.db import MyDB
from src.commands.commands import commandInit
from src.config import config
from src.events.getUserMessage import eventGetUserMessageInit

bot = telebot.TeleBot(token=config['botToken'])
my_db = MyDB(config)
botActions = BotActions(bot, my_db)


def catch(err, message=None):
    my_db.setLogs(err)

    if type(message) is str:
        print(f'ОШИБКА: {message}')
    elif message:
        bot.send_message(message.chat.id, ANSWER_BOT['error'], parse_mode='html')
    else:
        print(f"ОШИБКА: {''.join(err.args)}")


def sendResult(result_data, chat_id):
    """Отправить пользователям результат действий"""
    error = result_data.get('error')
    answer = result_data.get('answer')

    if error:
        bot.send_message(chat_id, error, parse_mode='html')
    elif answer:
        bot.send_message(chat_id, answer, parse_mode='html')


# Регистрация действий на кнопки
actionsInit(bot, my_db, sendResult)
# Регистрация команд бота
commandInit(bot, my_db)
# Оповещение психологов о подключении бота
botActions.welcomePsychologists()
# Регистрация обработчика всех сообщений от пользователя
eventGetUserMessageInit(bot, my_db, catch)

bot.polling(none_stop=True)
