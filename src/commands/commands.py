from src.actions.const import buttons_available_action_psychologist, buttons_available_action_user, buttons_quit
from src.answer.answer import ANSWER_BOT
from src.commands.const import COMMANDS, PRIVATE_COMMANDS
from src.commands.enums import ListCommands, ListPrivateCommands
from src.utils.utils import generateReplyMarkup


def commandInit(bot, my_db):
    def _value(enum_item):
        return ''.join(enum_item.value)

    @bot.message_handler(commands=[_value(ListCommands.START)])
    def _start(message):
        chat_id = message.chat.id
        list_data_buttons = []
        answer = ''
        reply_markup = None

        if message.chat.type == 'private':
            my_db.addNewChat(message.chat)

        is_psychologist = my_db.checkIsPsychologist(chat_id)

        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBYNxlJPtTTbW5HZEh-l-8FdXUEz11DAACZTUAAsG5CEkBLmVNHWv5WzAE')

        if is_psychologist:
            answer = ANSWER_BOT['all_commands_psychology']
            reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
        else:
            bot.send_message(chat_id, ANSWER_BOT['start'], parse_mode='html')
            answer = ANSWER_BOT['available_commands_user']
            reply_markup = generateReplyMarkup(buttons_available_action_user)

        bot.send_message(chat_id=chat_id, text=answer, reply_markup=reply_markup)

    @bot.message_handler(commands=[_value(ListCommands.INFO)])
    def _info(message):
        chat_id = message.chat.id

        bot.send_message(chat_id, ANSWER_BOT['about_bot'])

    @bot.message_handler(commands=[_value(ListCommands.HELP)])
    def _help(message):
        chat_id = message.chat.id
        commands = '\n'
        is_psychologist = my_db.checkIsPsychologist(chat_id)

        for command in COMMANDS:
            commands += f"/{''.join(command['command'])} - {command['description']}\n"

        if is_psychologist:
            commands += f"\nКак психологу вам доступны дополнительные команды:\n"
            for command in PRIVATE_COMMANDS:
                commands += f"/{''.join(command['command'])} - {command['description']}\n"

        bot.send_message(chat_id, 'Команды: ' + commands, parse_mode='html')

    @bot.message_handler(commands=[_value(ListCommands.QUIT)])
    def _quit(message):
        chat_id = message.chat.id
        is_psychologist = my_db.checkIsPsychologist(chat_id)
        reply_markup = generateReplyMarkup(buttons_quit)
        answer = ANSWER_BOT['quit']

        if is_psychologist:
            answer += ANSWER_BOT['quit_psychologist']
        else:
            answer += ANSWER_BOT['quit_user']

        bot.send_message(chat_id, answer, reply_markup=reply_markup)

    @bot.message_handler(commands=[_value(ListPrivateCommands.GET_ALL_COMMANDS_PSYCHOLOGISTS)])
    def _get_all_commands_psychology(message):
        chat_id = message.chat.id

        is_psychologist = my_db.checkIsPsychologist(chat_id)

        if not is_psychologist:
            return

        reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
        bot.send_message(chat_id=chat_id, text=ANSWER_BOT['all_commands_psychology'], reply_markup=reply_markup)
