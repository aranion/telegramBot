import json

import firebase_admin
from firebase_admin import credentials, db
from src.answer.answer import ANSWER_BOT


class MyDB:
    """Управление БД"""

    def __init__(self, config):
        try:
            if not config:
                raise ValueError('Не передан config')
            self.cred = credentials.Certificate(config['serviceAccount'])
            firebase_admin.initialize_app(self.cred, {'databaseURL': config['firebase']['databaseURL']})
            print('---INIT DB---')
        except ValueError as ex:
            print('Ошибка инициализации database', ex)

    @staticmethod
    def setLogs(err):
        try:
            print('MyDB->setLogs')

            ref_main = db.reference('/logs/')
            ref_main.push(f"Ошибка: {''.join(err.args)}")
        except Exception as ex:
            print('Ошибка при записи лога', ex)

    @staticmethod
    def addNewChat(chat):
        """Добавить новый чат, если он еще не добавлен"""
        try:
            print('MyDB->addNewChat')

            chat_id = chat.id
            ref_chats = db.reference('/chats/')
            data = ref_chats.get()

            if (not data) or (not data.get(str(chat_id))):
                new_data = ref_chats.child(f'{chat_id}')
                new_data.set({
                    'username': chat.username,
                    'first_name': chat.first_name,
                    'type': chat.type,
                    'id': chat_id,
                    'isPsychologist': False,
                    'is_next_message_psychologist': False
                })
                return
        except Exception as ex:
            print('Ошибка при добавлении нового чата', ex)

    @classmethod
    def addNewMessagePsychologist(cls, message):
        """Записать сообщение для психолога"""
        try:
            print('MyDB->addNewMessagePsychologist')

            chat_id = message.chat.id
            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Если это сообщение психолога, то записывать его не нужно
            if is_psychologist:
                return

            ref_main = db.reference('/')
            new_message = {'date': message.date, 'chat_id': chat_id, 'text': message.text}
            message_id = message.message_id

            new_data = ref_main.child(f'messagesPsychologist/{message_id}')
            new_data.set(new_message)

            cls.setIsNextMessagePsychologist(chat_id, False)
        except Exception as ex:
            print('Ошибка при записи сообщения для психолога в БД', ex)

    @classmethod
    def addCategory(cls, current_chat_id, name_category, parent_id_category=None):
        """Добавить новую категорию"""
        try:
            print('MyDB->addCategory')

            is_psychologist = cls.checkIsPsychologist(current_chat_id)

            # Только психологи могут добавлять категории
            if not is_psychologist:
                raise ValueError(ANSWER_BOT['not_access'])

            # Проверка на существование родительской категории
            if parent_id_category:
                ref_parent_categories = db.reference(f'/categories/{parent_id_category}')
                data_parent_categories = ref_parent_categories.get()

                if not data_parent_categories:
                    raise ValueError(f'{ANSWER_BOT["error_not_id_parent_category"]} {parent_id_category}')

            # Максимальная длина имени категории
            if len(name_category) > 30:
                raise ValueError(ANSWER_BOT['error_max_length_30'])

            ref_main = db.reference('/')
            ref_categories = db.reference('/categories/')
            data_categories = ref_categories.get()
            next_id_category = 0

            if data_categories:
                next_id_category = data_categories[-1:][0]['id'] + 1

            new_category_data = ref_main.child(f'categories/{next_id_category}')
            new_category_data.set({'id': next_id_category, 'name': name_category, 'parent_id': parent_id_category})

            return {'answer': f'Категория "{name_category}" успешно добавлена'}
        except ValueError as ex:
            print('Ошибка при добавлении новой категории', ex)
            return {'error': ex}

    @classmethod
    def addMessageInArchive(cls, chat_id, question):
        """Добавить ответ на вопрос отправленный психологом в архив чата"""
        try:
            print('MyDB->addMessageInArchive')

            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Если не психолог
            if not is_psychologist:
                return

            ref_chat = db.reference(f'/chats/{chat_id}/archive/')
            ref_chat.push(question)
        except Exception as ex:
            print('Ошибка при добавлении ответа на вопрос отправленный психологом в архив', ex)

    @classmethod
    def getMessagesInArchive(cls, chat_id):
        """Получить все сообщения из архива в чате психолога"""
        try:
            print('MyDB->getMessagesInArchive')

            ref_chat = db.reference(f'/chats/{chat_id}/archive/')
            data = ref_chat.get()

            return data
        except Exception as ex:
            print('Ошибка при получении ответа на вопрос отправленный психологом в архив', ex)

    @staticmethod
    def getAllPsychologists():
        """Получить всех психологов"""
        try:
            print('MyDB->getAllPsychologists')

            ref_chats = db.reference('/chats/')
            data = ref_chats.get()
            dict_all_psychologists = {}

            if not data:
                return dict_all_psychologists
            for chat_id in data:
                is_psychologist = data[chat_id].get('isPsychologist')
                if is_psychologist:
                    dict_all_psychologists[chat_id] = data[chat_id]
            return dict_all_psychologists
        except Exception as ex:
            print('Ошибка при получении всех психологов', ex)

    @classmethod
    def getMessagesPsychologist(cls, current_chat_id):
        """Получить все сообщения для психолога"""
        try:
            print('MyDB->getMessagesPsychologist')

            is_psychologist = cls.checkIsPsychologist(current_chat_id)

            if not is_psychologist:
                return ANSWER_BOT['not_access']

            ref_messages_psychologist = db.reference('/messagesPsychologist/')
            data = ref_messages_psychologist.get()

            return data
        except Exception as ex:
            print('Ошибка при получении всех сообщений психологу', ex)

    @classmethod
    def getMessagesPsychologistById(cls, message, message_id):
        """Получить сообщение для психолога по ID сообщения"""
        try:
            print('MyDB->getMessagesPsychologistById')

            is_psychologist = cls.checkIsPsychologist(message.chat.id)

            if not is_psychologist:
                return ANSWER_BOT['not_access']

            ref_messages_psychologist = db.reference(f'/messagesPsychologist/{message_id}')
            data = ref_messages_psychologist.get()

            return data
        except Exception as ex:
            print('Ошибка при получении сообщение для психолога по ID сообщения', ex)

    @classmethod
    def getIsNextMessagePsychologist(cls, chat_id):
        """Проверить является ли передаваемое сообщение для психолога"""
        try:
            print('MyDB->getIsNextMessagePsychologist')

            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Психолог не может сам себе отправлять сообщения...
            if is_psychologist:
                return False

            ref_is_next_message_psychologist = db.reference(f'/chats/{chat_id}/is_next_message_psychologist')
            data = ref_is_next_message_psychologist.get()

            return data
        except Exception as ex:
            print('Ошибка при проверки сообщения для психолога', ex)

    @classmethod
    def getCategories(cls, parent_id=None):
        """Получить все категории"""
        try:
            print('MyDB->getCategories')

            ref_categories = db.reference('/categories/')
            temp_data = ref_categories.get()
            data = []

            for item in temp_data:
                if parent_id:
                    # Подкатегории по ID
                    if 'parent_id' in item and int(parent_id) == int(item.get('parent_id')):
                        data.append(item)
                else:
                    # Категории верхнего уровня
                    if not ('parent_id' in item):
                        data.append(item)

            return data
        except Exception as ex:
            print('Ошибка при получении категорий', ex)

    @classmethod
    def getCategoryById(cls, category_id):
        """Получить категорию по ID"""
        try:
            print('MyDB->getCategoryById')

            ref_category = db.reference(f'/categories/{category_id}/')
            data = ref_category.get()

            return data
        except Exception as ex:
            print('Ошибка при получении категории по ID', ex)

    @classmethod
    def getQuestions(cls, category_id=None):
        """Получить все вопросы"""
        try:
            print('MyDB->getQuestion')

            ref_question = db.reference('/questions/')
            data = ref_question.get()

            if category_id:
                filter_data = []
                for question in data:
                    if int(question.get('category')) == int(category_id):
                        filter_data.append(question)
                return filter_data
            return data
        except Exception as ex:
            print('Ошибка при получении вопросов', ex)

    @classmethod
    def getQuestionById(cls, question_id):
        """Получить вопрос по ID"""
        try:
            print('MyDB->getQuestionById')

            ref_question = db.reference(f'/questions/{question_id}')
            data = ref_question.get()

            return data
        except Exception as ex:
            print('Ошибка при получении вопроса по ID', ex)

    @staticmethod
    def checkIsPsychologist(chat_id):
        """Проверить есть ли у пользователя права психолога"""
        try:
            print('MyDB->checkIsPsychologist')

            ref_chat = db.reference(f'/chats/{chat_id}/')

            data = ref_chat.get()
            if data:
                return data.get('isPsychologist')
            return False
        except Exception as ex:
            print('Ошибка при проверки на права психолога', ex)

    @classmethod
    def setMessage(cls, message):
        """Записать все произвольные сообщения пользователя(кроме сообщения психолога)"""
        try:
            print('MyDB->setMessage')
            chat_id = message.chat.id
            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Если это сообщение психолога, то добавлять его в DB не нужно
            if is_psychologist:
                return

            ref_messages = db.reference(f'/chats/{chat_id}/messages/')
            data = ref_messages.get()
            new_message = {'date': message.date, 'message_id': message.message_id, 'text': message.text}
            max_list_messages_in_db = 5

            if not data:
                data = []

            data.append(new_message)

            if data.__len__() > max_list_messages_in_db:
                data.pop(0)

            ref_messages.set(data)
        except Exception as ex:
            print('Ошибка при записи сообщения в БД', ex)

    @classmethod
    def setIsNextMessagePsychologist(cls, chat_id, is_value):
        """Установить что следующее сообщение будет направлено психологу"""
        try:
            print('MyDB->setIsNextMessagePsychologist')

            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Психолог не может сам себе отправлять сообщения...
            if is_psychologist:
                return

            ref_is_next_message_psychologist = db.reference(f'/chats/{chat_id}/is_next_message_psychologist')
            ref_is_next_message_psychologist.set(is_value)
        except Exception as ex:
            print('Ошибка установки переменной дял определения следующего сообщения психологу', ex)

    @classmethod
    def setPsychologistResponsible(cls, chat_id, message_id):
        """Взять в работу сообщение"""
        try:
            print('MyDB->setPsychologistResponsible')

            is_psychologist = cls.checkIsPsychologist(chat_id)

            # Только психолог может брать в работу сообщение
            if not is_psychologist:
                return

            ref_messages_psychologist = db.reference(f'/messagesPsychologist/{message_id}/')
            data_messages_psychologist = ref_messages_psychologist.get()

            if not data_messages_psychologist:
                raise ValueError(ANSWER_BOT['error_message_not_found'].format(message_id))

            ref_id_psychologist_responsible = db.reference(
                f'/messagesPsychologist/{message_id}/id_psychologist_responsible')
            data_id_psychologist_responsible = ref_id_psychologist_responsible.get()

            if data_id_psychologist_responsible:
                if data_id_psychologist_responsible == chat_id:
                    raise ValueError(ANSWER_BOT['error_you_get_message_in_work'])
                raise ValueError(ANSWER_BOT['error_message_get_other_psychologist'])

            ref_id_psychologist_responsible.set(chat_id)

            return {'answer': ANSWER_BOT['psychologist_responsible']}
        except Exception as ex:
            print('Ошибка назначении психолога ответственным за ответ пользователю', ex)
            return {'error': ex}

    @classmethod
    def deleteMessagePsychologistById(cls, message_id):
        """Удалить сообщение для психолога по id сообщения"""
        try:
            print('MyDB->deleteMessagePsychologistById')

            ref_messages_psychologist = db.reference(f'/messagesPsychologist/{message_id}')
            data = ref_messages_psychologist.get()

            if not data:
                raise ValueError(ANSWER_BOT['error_find_user_message_by_id'])

            ref_messages_psychologist.delete()

            return {'answer': ANSWER_BOT['successfully_message_psychologist_delete']}
        except ValueError as ex:
            print('Ошибка при удалении сообщения из БД', ex)
            return {'error': ex}
