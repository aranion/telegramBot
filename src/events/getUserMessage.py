from src.actions.enums import ListActions
from src.answer.answer import ANSWER_BOT
from src.utils.utils import generateReplyMarkup


def eventGetUserMessageInit(bot, my_db, catch):
    @bot.message_handler(content_types=['text'])
    def get_user_text(message):
        try:
            chat_id = message.chat.id
            is_psychology = my_db.checkIsPsychologist(chat_id)

            # Если сообщение отправляет психолог
            if is_psychology:
                # Проверяется наличие id сообщения в ответе психолога для ответа
                text = message.text
                list_str = text.strip().split(' ')

                try:
                    message_id = int(list_str.pop(0))
                    is_command_delete = list_str[0].strip().upper() == 'DELETE'
                    message_psychology = my_db.getMessagesPsychologyById(message, message_id)

                    # Если нет вопросов для психолога
                    if not message_psychology:
                        answer = ANSWER_BOT['error_find_user_message_by_id']
                        # И если это не команда на удаление
                        if not is_command_delete:
                            answer += ANSWER_BOT['error_message_id_in_message_psychology']
                        # Сообщить психологу, что вопрос не найден по ID
                        return bot.reply_to(message, answer)

                    if is_command_delete:
                        list_data_buttons = [
                            {
                                'text': 'Да!',
                                'action': ''.join(
                                    ListActions.DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS.value) + f'_ID_{message_id}',
                            },
                        ]
                        reply_markup = generateReplyMarkup(list_data_buttons)
                        answer = f'Вы хотите удалить?:\n\nID: {message_id}, Сообщение: \"{message_psychology["text"]}\"'
                        bot.send_message(chat_id=chat_id, text=answer, reply_markup=reply_markup)
                    else:
                        answer_psychology_string = ' '.join(list_str)
                        answer = f"""{ANSWER_BOT['send_question']}\n\n<b>Вопрос</b>: \"{message_psychology['text']}\"\n<b>Ответ</b>: \"{answer_psychology_string}\""""
                        # Ответ для пользователя
                        bot.send_message(message_psychology['chat_id'], answer, parse_mode='html')
                        # Ответ для психолога
                        bot.send_message(chat_id, ANSWER_BOT['successfully_sent'], parse_mode='html')
                        # Вопрос удаляется из БД, для предотвращения повторного ответа
                        my_db.deleteMessagePsychologyById(message_id)
                        # TODO Предоставить возможность психологу изменить отправленное сообщение...
                        # TODO может быть стоит помечать их как отвеченные, а не удалять...
                except ValueError as ex:
                    bot.reply_to(message, ANSWER_BOT['error_message_id_in_answer_psychology'])
                    print(ANSWER_BOT['error_message_id_in_answer_psychology'], ex)
            else:
                is_next_message_psychology = my_db.getIsNextMessagePsychology(chat_id)

                # Записываются все сообщения от пользователя (стоит ограничение только последние 5шт)
                my_db.setMessage(message)

                # Если сообщение адресовано психологу
                if is_next_message_psychology:
                    # Получаем всех психологов
                    all_psychologists = my_db.getAllPsychologists()
                    # Формируем сообщение для психолога
                    new_user_message = f'ID: {message.message_id}\nСообщение: "{message.text}"'

                    # Добавить новое сообщение для психолога в БД
                    my_db.addNewMessagePsychology(message)

                    # Отправить поступившее сообщение с вопросом в чаты психологов
                    for psychologist in all_psychologists:
                        # TODO Нужно распределить сообщения между всеми психологами, не всем сразу
                        bot.send_message(psychologist, ANSWER_BOT['new_message_received'], parse_mode='html')
                        bot.send_message(psychologist, new_user_message, parse_mode='html')

                    # Уведомить пользователя об успешной отправки сообщения
                    bot.reply_to(message, ANSWER_BOT['send_message_psychology'])
                else:
                    bot.reply_to(message, ANSWER_BOT['no_understand'])
        except Exception as ex:
            catch(ex)

    @bot.message_handler()
    # @bot.message_handler(content_types=['photo', 'audio', 'sticker', 'document', 'video', 'video_note', 'voice', 'location', 'contact', ''])
    def get_user_other(message):
        bot.send_message(message.chat.id, ANSWER_BOT['i_dont_know_format_file'])
