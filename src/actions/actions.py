import re

from src.actions.const import buttons_available_action_user, ALL_BUTTONS
from src.answer.answer import ANSWER_BOT
from src.utils.utils import generateReplyMarkup, getValueEnum


def actionsInit(bot, my_db, sendResult):
    """Регистрация действий при нажатии кнопок"""

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            # Если сообщение из чата с ботом
            if call.message:
                type_action = call.data
                chat_id = call.message.chat.id

                if type_action == getValueEnum('SEND_MESSAGE_PSYCHOLOGISTS'):
                    # Действие "Написать психологу"
                    reply_markup = generateReplyMarkup([ALL_BUTTONS['CANCEL_SEND_MESSAGE_PSYCHOLOGISTS']])

                    my_db.setIsNextMessagePsychologist(chat_id, True)

                    return bot.send_message(chat_id, ANSWER_BOT['next_message_psychologist'], reply_markup=reply_markup)
                elif type_action == getValueEnum('CANCEL_SEND_MESSAGE_PSYCHOLOGISTS'):
                    # Действие "Отменить "Написать психологу""
                    reply_markup = generateReplyMarkup(buttons_available_action_user)
                    is_next_message_psychologist = my_db.getIsNextMessagePsychologist(chat_id)

                    if is_next_message_psychologist:
                        my_db.setIsNextMessagePsychologist(chat_id, False)
                        answer = ANSWER_BOT['next_message_psychologist_end']

                        return bot.send_message(chat_id, answer, reply_markup=reply_markup)
                    return
                elif type_action == getValueEnum('GET_ALL_UNALLOCATED_MESSAGES_FOR_PSYCHOLOGISTS'):
                    # Кнопка "Все нераспределенные сообщения"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    messages_psychologist = my_db.getMessagesPsychologist(chat_id)

                    bot.send_message(chat_id, ANSWER_BOT['all_unallocated_message'], parse_mode='html')

                    if messages_psychologist:
                        is_not_message = True

                        for key in messages_psychologist:
                            value = messages_psychologist[key]

                            if not value.get('id_psychologist_responsible'):
                                is_not_message = False
                                answer = f'✉️ ID: <code>{key}</code>, Сообщение: \"{value.get("text")}\"\n'
                                buttons_list_data = [{
                                    'text': 'Взять в работу',
                                    'action': f'{getValueEnum("SET_PSYCHOLOGIST_RESPONSIBLE")}_ID_{key}'
                                }]
                                reply_markup = generateReplyMarkup(buttons_list_data)
                                bot.send_message(chat_id, answer, parse_mode='html', reply_markup=reply_markup)

                        if is_not_message:
                            return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                        return
                    else:
                        return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                elif type_action == getValueEnum('GET_TEN_RESPONSIBLE_MESSAGES_FOR_PSYCHOLOGISTS'):
                    # Кнопка "Взятые в работу сообщения"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    messages_psychologist = my_db.getMessagesPsychologist(chat_id)

                    bot.send_message(chat_id, ANSWER_BOT['responsible_for_message'], parse_mode='html')

                    if messages_psychologist:
                        index = 1
                        is_not_message = True

                        for key in messages_psychologist:
                            value = messages_psychologist[key]

                            if value.get('id_psychologist_responsible') == chat_id:
                                is_not_message = False

                                # Показать только первые 10 сообщений
                                if index > 10:
                                    return bot.send_message(chat_id, ANSWER_BOT['show_first_10_message'])
                                answer = f'✉️ ID: <code>{key}</code>, Сообщение: \"{value["text"]}\"'
                                bot.send_message(chat_id, answer, parse_mode='html')

                                ++index

                        if is_not_message:
                            return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                        return bot.send_message(chat_id, ANSWER_BOT['send_answer_for_user'])
                    return bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                elif type_action == getValueEnum('GET_ALL_PSYCHOLOGISTS'):
                    # Кнопка "Получить всех психологов"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    all_psychologists = my_db.getAllPsychologists()
                    answer = ANSWER_BOT['list_psychologist']

                    for key in all_psychologists:
                        value = all_psychologists[key]
                        id_psychologist = value.get("id")
                        first_name_psychologist = value.get("first_name")
                        username = ''

                        if value.get("username"):
                            username += f'({value.get("username")})'

                        answer += f'ID: <code>{id_psychologist}</code>, Имя: \"{first_name_psychologist}\"{username}\n'

                    return bot.send_message(chat_id, answer, parse_mode='html')
                elif type_action == getValueEnum('GET_ALL_USERS'):
                    # Кнопка "Список пользователей"
                    # TODO т.к. система должна быть "анонимной", получать всех пользователей не правильно...
                    return None
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    all_users = my_db.getUsers(chat_id)
                    answer = ANSWER_BOT['list_users']

                    for key in all_users:
                        value = all_users[key]
                        id_users = value.get("id")
                        first_name_psychologist = value.get("first_name")
                        username = ''

                        if value.get("username"):
                            username += f'({value.get("username")})'

                        answer += f'ID: <code>{id_users}</code>, Имя: \"{first_name_psychologist}\"{username}\n'

                    return bot.send_message(chat_id, answer, parse_mode='html')
                elif type_action == getValueEnum('GET_ARCHIVE_MESSAGE_PSYCHOLOGIST'):
                    # Кнопка "Получить все архивные сообщения"
                    message_archive = my_db.getMessagesInArchive(chat_id)

                    bot.send_message(chat_id, ANSWER_BOT['archive_info'], parse_mode='html')

                    if not message_archive:
                        bot.send_message(chat_id, ANSWER_BOT['not_messages'])
                    else:
                        for key in message_archive:
                            value = message_archive[key]
                            answer = f'<b>Вопрос:</b>\n\"{value.get("text")}\"\n<b>Ответ:</b>\n\"<code>{value.get("answer")}</code>\"'
                            bot.send_message(chat_id, answer, parse_mode='html')
                    return
                elif re.search(f'^{getValueEnum("GET_ANSWER_QUESTION_FROM_CATEGORY")}(_ID_\d+)?$', type_action):
                    id_re = re.search('_ID_\d+', type_action)

                    if id_re:
                        list_str = id_re.group().split('_')
                        question_id = int(list_str[-1:][0])
                        question = my_db.getQuestionById(question_id)
                        question_answer = '\n'.join(question.get("answer").split('\\n'))
                        answer = f'<b>Вопрос</b>:\n\"{question.get("text")}\"\n\n<b>Ответ</b>:\n\"{question_answer}\"'
                        reply_markup = generateReplyMarkup([ALL_BUTTONS['SEARCH_OTHER_CATEGORIES']])
                        return bot.send_message(chat_id, answer, parse_mode='html', reply_markup=reply_markup)
                    return
                elif type_action == getValueEnum('ADD_NEW_CATEGORY'):
                    # Кнопка "Добавить новую подкатегорию"
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    # sendResult(my_db.addCategory(chat_id, message.text), chat_id)

                    return bot.send_message(chat_id, ANSWER_BOT['i_dont_know_actions'])
                elif re.search(f'^{getValueEnum("SET_PSYCHOLOGIST_RESPONSIBLE")}(_ID_\d+)?$', type_action):
                    # Кнопка "Взять в работу"
                    re_message_id = re.search('_ID_\d+', type_action)

                    if re_message_id:
                        list_str = re_message_id.group().split('_')
                        message_id = list_str[-1:][0]
                        sendResult(my_db.setPsychologistResponsible(chat_id, message_id), chat_id)
                    return
                elif re.search(f'^{getValueEnum("SET_USERS_IS_PSYCHOLOGISTS")}(_ID_(\d+))?$', type_action):
                    re_id_psychologist = re.search('_ID_(\d+)', type_action)

                    if re_id_psychologist:
                        list_str = re_id_psychologist.group().split('_')
                        psychologist_id = list_str[-1:][0]

                        return sendResult(my_db.setIsPsychologist(chat_id, psychologist_id), chat_id)
                    return bot.send_message(chat_id, 'Введен не корректный ID чата')
                elif re.search(f'^{getValueEnum("DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS")}(_ID_\d+)?$', type_action):
                    # Кнопка "Удалить вопрос по ID"
                    id_message_delete_re = re.search('_ID_\d+', type_action)
                    is_psychologist = my_db.checkIsPsychologist(chat_id)

                    if not is_psychologist:
                        return bot.send_message(chat_id, ANSWER_BOT['not_access'])

                    if id_message_delete_re:
                        list_str = id_message_delete_re.group().split('_')
                        message_id = int(list_str[-1:][0])

                        return sendResult(my_db.deleteMessagePsychologistById(message_id), chat_id)
                    return bot.send_message(chat_id, ANSWER_BOT['how_delete_message_by_id'])
                elif re.search(f'^{getValueEnum("SEARCH_CATEGORY")}(_NEXT_(\d+))?$', type_action):
                    next_re = re.search('_NEXT_(\d+)', type_action)
                    list_buttons = []
                    answer = ANSWER_BOT['select_category']
                    current_category_id = None
                    number_column = 1

                    if next_re:
                        # Если указан следующая подкатегория
                        list_str = next_re.group().split('_')
                        current_category_id = list_str[-1:][0]
                        categories = my_db.getCategories(current_category_id)
                    else:
                        # Иначе оказать все без категории
                        answer = ANSWER_BOT['select_section']
                        categories = my_db.getCategories()

                    # Подготовить кнопки категорий
                    for category in categories:
                        text = category.get('name')
                        action = f'{getValueEnum("SEARCH_CATEGORY")}_NEXT_{category.get("id")}'
                        list_buttons.append({'text': text, 'action': action})

                    # Если категорий нет, значит нужно показывать вопросы
                    if len(categories) == 0:
                        answer = ANSWER_BOT['select_suitable_question']
                        questions = my_db.getQuestions(current_category_id)

                        if len(questions) == 0:
                            answer = ANSWER_BOT['sorry_category_empty']
                            list_buttons = buttons_available_action_user
                        for item in questions:
                            question = item.get('text')
                            action = f'{getValueEnum("GET_ANSWER_QUESTION_FROM_CATEGORY")}_ID_{item.get("id")}'
                            list_buttons.append({'text': question, 'action': action})
                    else:
                        # Добавить кнопку "Назад"
                        if current_category_id:
                            parent_category = my_db.getCategoryById(current_category_id)
                            parent_category_id = parent_category.get('parent_id')
                            text = "<-- Назад"
                            action = getValueEnum("SEARCH_CATEGORY")

                            if parent_category_id:
                                action += f'_NEXT_{parent_category_id}'
                            list_buttons.append({'text': text, 'action': action})

                        if len(categories) > 2:
                            number_column = 2
                    reply_markup = generateReplyMarkup(list_buttons, number_column)
                    return bot.send_message(chat_id, answer, reply_markup=reply_markup)
                else:
                    bot.send_message(chat_id, ANSWER_BOT['i_dont_know_actions'])
            elif call.inline_message_id:
                # Если сообщение из инлайн-режима
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=ANSWER_BOT['actions_i_dont_know'])
        except Exception as ex:
            print('Ошибка при выполнении действия', ex)
            bot.send_message(call.message.chat.id, ANSWER_BOT['error'], parse_mode='html')
