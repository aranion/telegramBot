from src.utils.utils import getValueEnum

ALL_BUTTONS = {
    'ALL_PSYCHOLOGISTS': {
        'text': 'Список психологов 😎',
        'action': getValueEnum('GET_ALL_PSYCHOLOGISTS')
    },
    'ALL_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Получить все неотвеченные сообщения ✉️',
        'action': getValueEnum('GET_ALL_MESSAGES_FOR_PSYCHOLOGISTS')
    },
    'ARCHIVE_MESSAGE_PSYCHOLOGIST': {
        'text': 'Архивные сообщения 📦',
        'action': getValueEnum('GET_ARCHIVE_MESSAGE_PSYCHOLOGIST')
    },
    'TEN_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Получить 10 последних сообщения 📬',
        'action': getValueEnum('GET_TEN_MESSAGES_FOR_PSYCHOLOGISTS')
    },
    'DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS': {
        'text': 'Удалить сообщение пользователя ❌',
        'action': getValueEnum('DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS')
    },
    'SEARCH_CATEGORY': {
        'text': 'Самостоятельно поискать ответ на вопрос 🔍',
        'action': getValueEnum('SEARCH_CATEGORY')
    },
    'NEW_CATEGORY': {
        'text': 'Добавить новую категорию ➕',
        'action': getValueEnum('ADD_NEW_CATEGORY')
    },
    'SEND_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Задать вопрос психологу 📝',
        'action': getValueEnum('SEND_MESSAGE_PSYCHOLOGISTS')
    },
    'CANCEL_SEND_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Не сейчас',
        'action': getValueEnum('CANCEL_SEND_MESSAGE_PSYCHOLOGISTS'),
    },
    'DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS': {
        'text': 'Удалить сообщение по ID ❌',
        'action': getValueEnum('DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS'),
    },
    'QUIT': {
        'text': 'Выйти',
        'action': getValueEnum('QUIT')
    },
    'SEARCH_OTHER_CATEGORIES': {
        'text': '🔍 Найти другой вопрос',
        'action': getValueEnum('SEARCH_CATEGORY')
    }
}

# Доступные действия для психологов:
buttons_available_action_psychologist = [
    ALL_BUTTONS['ALL_MESSAGE_PSYCHOLOGISTS'],
    ALL_BUTTONS['TEN_MESSAGE_PSYCHOLOGISTS'],
    ALL_BUTTONS['ARCHIVE_MESSAGE_PSYCHOLOGIST'],
    ALL_BUTTONS['ALL_PSYCHOLOGISTS'],
    ALL_BUTTONS['DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS'],
    ALL_BUTTONS['NEW_CATEGORY'],
    ALL_BUTTONS['SEARCH_CATEGORY'],
]
# Доступные действия для пользователя
buttons_available_action_user = [
    ALL_BUTTONS['SEARCH_CATEGORY'],
    ALL_BUTTONS['SEND_MESSAGE_PSYCHOLOGISTS'],
]

buttons_quit = [
    ALL_BUTTONS['QUIT']
]
