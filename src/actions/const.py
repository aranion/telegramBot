from src.actions.enums import ListActions

ALL_BUTTONS = {
    'ALL_PSYCHOLOGISTS': {
        'text': 'Список психологов',
        'action': ListActions.GET_ALL_PSYCHOLOGISTS.value
    },
    'ALL_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Получить все неотвеченные сообщения',
        'action': ListActions.GET_ALL_MESSAGES_FOR_PSYCHOLOGISTS.value
    },
    'ARCHIVE_MESSAGE_PSYCHOLOGIST': {
        'text': 'Архивные сообщения',
        'action': ListActions.GET_ARCHIVE_MESSAGE_PSYCHOLOGIST.value
    },
    'TEN_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Получить 10 последних сообщения',
        'action': ListActions.GET_TEN_MESSAGES_FOR_PSYCHOLOGISTS.value
    },
    'DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS': {
        'text': 'Удалить сообщение пользователя',
        'action': ListActions.DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS.value
    },
    'SEARCH_CATEGORY': {
        'text': 'Самостоятельно найти ответ на вопрос',
        'action': ListActions.SEARCH_CATEGORY.value
    },
    'NEW_CATEGORY': {
        'text': 'Добавить новую категорию',
        'action': ListActions.ADD_NEW_CATEGORY.value
    },
    'SEND_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Задать вопрос психологу',
        'action': ListActions.SEND_MESSAGE_PSYCHOLOGISTS.value
    },
    'CANCEL_SEND_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Не сейчас',
        'action': ListActions.CANCEL_SEND_MESSAGE_PSYCHOLOGISTS.value,
    },
    'DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS': {
        'text': 'Удалить сообщение по ID',
        'action': ListActions.DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS.value,
    },
    'QUIT': {
        'text': 'Выйти',
        'action': ListActions.QUIT.value
    },
    'SEARCH_OTHER_CATEGORIES': {
        'text': 'Найти другой вопрос',
        'action': ListActions.SEARCH_CATEGORY.value
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
