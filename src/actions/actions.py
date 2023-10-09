import re

from src.actions.const import buttons_available_action_user, ALL_BUTTONS
from src.actions.enums import ListActions
from src.answer.answer import ANSWER_BOT
from src.utils.utils import generateReplyMarkup


def actionsInit(bot, my_db, sendResult):
    """Регистрация действий при нажатии кнопок"""

    def _value(enum_item):
        return ''.join(enum_item.value)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            # Если сообщение из чата с ботом
            if call.message:
                type_action = call.data
                chat_id = call.message.chat.id

                if type_action == _value(ListActions.SEND_MESSAGE_PSYCHOLOGISTS):
                    # Действие "Написать психологу"
                    reply_markup = generateReplyMarkup([ALL_BUTTONS['CANCEL_SEND_MESSAGE_PSYCHOLOGISTS']])

                    my_db.setIsNextMessagePsychology(chat_id, True)

                    return bot.send_message(chat_id, ANSWER_BOT['next_message_psychology'], reply_markup=reply_markup)
                elif type_action == _value(ListActions.CANCEL_SEND_MESSAGE_PSYCHOLOGISTS):
                    # Действие "Отменить "Написать психологу""
                    reply_markup = generateReplyMarkup(buttons_available_action_user)
                    is_next_message_psychology = my_db.getIsNextMessagePsychology(chat_id)

                    if is_next_message_psychology:
                        my_db.setIsNextMessagePsychology(chat_id, False)
                        answer = ANSWER_BOT['next_message_psychology_end']

                        return bot.send_message(chat_id, answer, reply_markup=reply_markup)
                    return
                elif type_action == _value(ListActions.GET_ALL_MESSAGES_FOR_PSYCHOLOGISTS):
                    # Кнопка "Получить все сообщения для психолога"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)
                    answer = 'Сообщения:\n'

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    messages_psychology = my_db.getMessagesPsychology(chat_id)

                    if messages_psychology:
                        for key in messages_psychology:
                            answer += f'Id: {key}, Сообщение: \"{messages_psychology[key]["text"]}\"\n'

                        answer += f'\n{ANSWER_BOT["send_user_question"]}'
                        return bot.send_message(chat_id, answer)
                    else:
                        return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                elif type_action == _value(ListActions.GET_TEN_MESSAGES_FOR_PSYCHOLOGISTS):
                    # Кнопка "Получить последних 10 вопросов"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    messages_psychology = my_db.getMessagesPsychology(chat_id)

                    if messages_psychology:
                        index = 1

                        for key in messages_psychology:
                            # Показать только первые 10 сообщений
                            if index > 10:
                                return bot.send_message(chat_id, ANSWER_BOT['show_first_10_message'])
                            answer = f'Id: {key}, Сообщение: \"{messages_psychology[key]["text"]}\"'
                            bot.send_message(chat_id, answer)

                            ++index
                        return bot.send_message(chat_id, ANSWER_BOT['send_user_question'])
                    else:
                        return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                elif type_action == _value(ListActions.GET_ALL_PSYCHOLOGISTS):
                    # Кнопка "Получить всех психологов"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    all_psychologists = my_db.getAllPsychologists()
                    answer = 'Список психологов:\n'

                    for key in all_psychologists:
                        id_psychologist = all_psychologists[key].get("id")
                        first_name_psychologist = all_psychologists[key].get("first_name")

                        answer += f'Id: {id_psychologist}, Имя: \"{first_name_psychologist}\"\n'
                    return bot.send_message(chat_id, answer)
                elif type_action == _value(ListActions.ADD_NEW_CATEGORY):
                    # Кнопка "Добавить новую подкатегорию"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    return bot.send_message(chat_id, 'Пока не могу...')
                elif re.search(f'^{_value(ListActions.DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS)}(_ID_\d+)?$', type_action):
                    # Кнопка "Удалить вопрос по ID"
                    id_message_delete_re = re.search('_ID_\d+', type_action)
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    if id_message_delete_re:
                        list_str = id_message_delete_re.group().split('_')
                        message_id = int(list_str[-1:][0])

                        return sendResult(my_db.deleteMessagePsychologyById(message_id), chat_id)
                    return bot.send_message(chat_id, ANSWER_BOT['how_delete_question_by_id'])
                elif re.search(f'^{_value(ListActions.SEARCH_CATEGORY)}((_NEXT_|_BACK_)\d+)?$', type_action):
                    next_re = re.search('_NEXT_\d+', type_action)
                    back_re = re.search('_BACK_\d+', type_action)
                    list_data_buttons = []
                    categories = []
                    answer = ANSWER_BOT['select_category']

                    if next_re or back_re:
                        if back_re:
                            list_str = back_re.group().split('_')
                            back_id = int(list_str[-1:][0]) - 1
                            categories = my_db.getCategories(back_id)
                        else:
                            list_str = next_re.group().split('_')
                            next_id = list_str[-1:][0]
                            categories = my_db.getCategories(next_id)
                    else:
                        categories = my_db.getCategories()

                    for category in categories:
                        btn = {
                            'text': category.get('name'),
                            'action': f'{"".join(ListActions.SEARCH_CATEGORY.value)}_NEXT_{category.get("id")}',
                        }

                        list_data_buttons.append(btn)

                    if len(list_data_buttons) == 0:
                        answer = 'Подкатегорий нет, тут должны быть вопросы....'

                    # НАЗАД
                    if next_re:
                        list_str = next_re.group().split('_')
                        current_id = [len(list_str) - 1][0]
                        back_id = current_id - 1

                        if back_id <= 0:
                            back_id = 0

                        if back_id != 0:
                            btn = {
                                'text': "<- Назад",
                                'action': f'{"".join(ListActions.SEARCH_CATEGORY.value)}_BACK_{back_id}',
                            }

                            list_data_buttons.append(btn)

                    reply_markup = generateReplyMarkup(list_data_buttons)

                    return bot.send_message(chat_id, answer, reply_markup=reply_markup)
                else:
                    bot.send_message(call.message.chat.id, ANSWER_BOT['i_dont_know_actions'], parse_mode='html')
            elif call.inline_message_id:
                # Если сообщение из инлайн-режима
                bot.edit_message_text(inline_message_id=call.inline_message_id, text="Действия которое я не знаю...")
        except Exception as ex:
            print('Ошибка при выполнении действия', ex)
            bot.send_message(call.message.chat.id, ANSWER_BOT['error'], parse_mode='html')
