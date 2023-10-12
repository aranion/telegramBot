from src.actions.const import buttons_available_action_user
from src.actions.enums import ListActions
from src.answer.answer import ANSWER_BOT
from src.utils.utils import generateReplyMarkup, getValueEnum


def eventGetUserMessageInit(bot, my_db, catch):
    @bot.message_handler(content_types=['text'])
    def get_user_text(message):
        try:
            chat_id = message.chat.id
            is_psychologist = my_db.checkIsPsychologist(chat_id)

            # Если сообщение отправляет психолог
            if is_psychologist:
                # Проверяется наличие id сообщения в ответе психолога для ответа
                text = message.text
                list_str = text.strip().split(' ')

                try:
                    message_id = int(list_str.pop(0))
                    is_command_delete = list_str[0].strip().upper() == 'DELETE'
                    message_psychologist = my_db.getMessagesPsychologistById(message, message_id)

                    # Если нет вопросов для психолога
                    if not message_psychologist:
                        answer = ANSWER_BOT['error_find_user_message_by_id']
                        # И если это не команда на удаление
                        if not is_command_delete:
                            answer += ANSWER_BOT['error_message_id_in_message_psychologist']
                        # Сообщить психологу, что вопрос не найден по ID
                        return bot.reply_to(message, answer)

                    if is_command_delete:
                        list_data_buttons = [
                            {
                                'text': 'Да!',
                                'action': getValueEnum('DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS') + f'_ID_{message_id}'
                            },
                        ]
                        reply_markup = generateReplyMarkup(list_data_buttons)
                        answer = f'Вы хотите удалить?:\n\nID: {message_id}, Сообщение: \"{message_psychologist["text"]}\"'
                        bot.send_message(chat_id=chat_id, text=answer, reply_markup=reply_markup)
                    else:
                        answer_psychologist_string = ' '.join(list_str)
                        answer = f"""{ANSWER_BOT['send_question']}\n\n<b>Вопрос</b>:\n\"{message_psychologist['text']}\"\n<b>Ответ</b>:\n\"{answer_psychologist_string}\""""
                        # Ответ для пользователя
                        bot.send_message(message_psychologist['chat_id'], answer, parse_mode='html')
                        # Ответ для психолога
                        bot.send_message(chat_id, ANSWER_BOT['successfully_sent'], parse_mode='html')
                        # Вопрос удаляется из БД, для предотвращения повторного ответа
                        my_db.deleteMessagePsychologistById(message_id)
                        # Записать ответ в чат психолога, для дальнейшего управления и использования
                        data = {
                            'text': message_psychologist['text'],
                            'message_id': message_id,
                            'answer': answer_psychologist_string
                        }
                        my_db.addMessageInArchive(chat_id, data)
                        # TODO Предоставить возможность психологу изменить отправленное сообщение...
                        # TODO Спрашивать психолога об корректности отправляемого сообщения!
                except ValueError as ex:
                    bot.reply_to(message, ANSWER_BOT['error_message_id_in_answer_psychologist'])
                    print(ANSWER_BOT['error_message_id_in_answer_psychologist'], ex)
            else:
                is_next_message_psychologist = my_db.getIsNextMessagePsychologist(chat_id)

                # Записываются все сообщения от пользователя (стоит ограничение только последние 5шт)
                my_db.setMessage(message)

                # Если сообщение адресовано психологу
                if is_next_message_psychologist:
                    # Получаем всех психологов
                    all_psychologists = my_db.getAllPsychologists()
                    # Формируем сообщение для психолога
                    new_user_message = f'{ANSWER_BOT["new_message_received"]}:\nID: <code>{message.message_id}</code>\nСообщение: "{message.text}"'

                    # Добавить новое сообщение для психолога в БД
                    my_db.addNewMessagePsychologist(message)

                    # Отправить поступившее сообщение с вопросом в чаты психологов
                    for psychologist in all_psychologists:
                        buttons_list_data = [{
                            'text': 'Взять в работу',
                            'action': f'{getValueEnum("PSYCHOLOGIST_RESPONSIBLE")}_ID_{message.message_id}'
                        }]
                        reply_markup = generateReplyMarkup(buttons_list_data)
                        bot.send_message(psychologist, new_user_message, parse_mode='html', reply_markup=reply_markup)

                    # Уведомить пользователя об успешной отправки сообщения
                    bot.reply_to(message, ANSWER_BOT['send_message_psychologist'])
                else:
                    reply_markup = generateReplyMarkup(buttons_available_action_user)
                    bot.reply_to(message, ANSWER_BOT['no_understand'], reply_markup=reply_markup)
        except Exception as ex:
            catch(ex)

    @bot.message_handler()
    # @bot.message_handler(content_types=['photo', 'audio', 'sticker', 'document', 'video', 'video_note', 'voice', 'location', 'contact', ''])
    def get_user_other(message):
        bot.send_message(message.chat.id, ANSWER_BOT['i_dont_know_format_file'])
