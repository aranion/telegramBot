from src.actions.const import buttons_available_action_psychologist, buttons_available_action_user
from src.actions.enums import ListActions
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
        photo = open('..\\resources\\imgs\\logo.png', 'rb')
        list_data_buttons = []
        answer = ''
        reply_markup = None

        if message.chat.type == 'private':
            my_db.addNewChat(message.chat)

        is_psychologist = my_db.checkIsPsychologist(chat_id)

        bot.send_sticker(chat_id, ANSWER_BOT['start_sticky'])
        # bot.send_photo(chat_id, photo)
        bot.send_message(chat_id, ANSWER_BOT['start'], parse_mode='html')

        if is_psychologist:
            answer = 'Доступные действия для психологов:'
            reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
        else:
            answer = 'Вы можете задать вопрос специалисту или найти ответ в моей базе вопросов:'
            reply_markup = generateReplyMarkup(buttons_available_action_user)

        bot.send_message(chat_id=chat_id, text=answer, reply_markup=reply_markup)

    @bot.message_handler(commands=[_value(ListCommands.INFO)])
    def _info(message):
        chat = message.chat

        bot.send_message(chat.id, ANSWER_BOT['about_bot'])

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

        bot.send_message(chat_id, 'Доступные команды: ' + commands, parse_mode='html')

    @bot.message_handler(commands=[_value(ListCommands.QUIT)])
    def _quit(message):
        chat_id = message.chat.id
        is_psychologist = my_db.checkIsPsychologist(chat_id)
        reply_markup = generateReplyMarkup([{
            'text': 'Выйти',
            'action': '----'
        }])
        answer = 'TODO: Вы уверены что хотите покинуть чат?'

        if is_psychologist:
            answer += ' Ваши права как психолога будут удалены!'
        else:
            answer += ' Все ваши не отвеченные вопросы будут удалены!'

        bot.send_message(chat_id, answer, reply_markup=reply_markup)

    @bot.message_handler(commands=[_value(ListPrivateCommands.GET_ALL_COMMANDS_PSYCHOLOGISTS)])
    def _get_all_commands_psychology(message):
        chat_id = message.chat.id

        is_psychologist = my_db.checkIsPsychologist(chat_id)

        if not is_psychologist:
            return

        reply_markup = generateReplyMarkup(buttons_available_action_psychologist)
        bot.send_message(chat_id=chat_id, text='Доступные команды:', reply_markup=reply_markup)
