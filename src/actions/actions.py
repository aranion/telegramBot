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

                        answer += f'\n{ANSWER_BOT["send_answer_for_user"]}'
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
                        return bot.send_message(chat_id, ANSWER_BOT['send_answer_for_user'])
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

                    # sendResult(my_db.addCategory(chat_id, message.text), chat_id)

                    return bot.send_message(chat_id, 'Пока не умею 🫤')
                elif type_action == _value(ListActions.QUIT):
                    # Кнопка "Выход из чата"
                    return bot.send_message(chat_id, 'Пока не могу 😓')
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
                    return bot.send_message(chat_id, ANSWER_BOT['how_delete_message_by_id'])
                elif re.search(f'^{_value(ListActions.ANSWER_QUESTION_FROM_CATEGORY)}(_ID_\d+)?$', type_action):
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
                elif re.search(f'^{_value(ListActions.SEARCH_CATEGORY)}(_NEXT_(\d+))?$', type_action):
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
                        action = f'{_value(ListActions.SEARCH_CATEGORY)}_NEXT_{category.get("id")}'
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
                            action = f'{_value(ListActions.ANSWER_QUESTION_FROM_CATEGORY)}_ID_{item.get("id")}'
                            list_buttons.append({'text': question, 'action': action})
                    else:
                        # Добавить кнопку "Назад"
                        if current_category_id:
                            parent_category = my_db.getCategoryById(current_category_id)
                            parent_category_id = parent_category.get('parent_id')
                            text = "<-- Назад"
                            action = _value(ListActions.SEARCH_CATEGORY)

                            if parent_category_id:
                                action += f'_NEXT_{parent_category_id}'
                            list_buttons.append({'text': text, 'action': action})

                        if len(categories) > 2:
                            number_column = 2
                    reply_markup = generateReplyMarkup(list_buttons, number_column)
                    return bot.send_message(chat_id, answer, reply_markup=reply_markup)
            elif call.inline_message_id:
                # Если сообщение из инлайн-режима
                bot.edit_message_text(inline_message_id=call.inline_message_id, text=ANSWER_BOT['actions_i_dont_know'])
        except Exception as ex:
            print('Ошибка при выполнении действия', ex)
            bot.send_message(call.message.chat.id, ANSWER_BOT['error'], parse_mode='html')
