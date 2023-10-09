from src.actions.enums import ListActions

ALL_BUTTONS = {
    'ALL_PSYCHOLOGISTS': {
        'text': 'Список психологов',
        'action': ListActions.GET_ALL_PSYCHOLOGISTS.value
    },
    'ALL_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Получить все сообщения',
        'action': ListActions.GET_ALL_MESSAGES_FOR_PSYCHOLOGISTS.value
    },
    'TEN_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Получить 10 последних сообщения',
        'action': ListActions.GET_TEN_MESSAGES_FOR_PSYCHOLOGISTS.value
    },
    'DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS': {
        'text': 'Удалить сообщение пользователя по ID',
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
        'text': 'Задать вопрос специалисту',
        'action': ListActions.SEND_MESSAGE_PSYCHOLOGISTS.value
    },
    'CANCEL_SEND_MESSAGE_PSYCHOLOGISTS': {
        'text': 'Отмена',
        'action': ListActions.CANCEL_SEND_MESSAGE_PSYCHOLOGISTS.value,
    },
    'DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS': {
        'text': 'Удалить сообщение по ID',
        'action': ListActions.DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS.value,
    },
}

# Доступные действия для психологов:
buttons_available_action_psychologist = [
    ALL_BUTTONS['ALL_PSYCHOLOGISTS'],
    ALL_BUTTONS['ALL_MESSAGE_PSYCHOLOGISTS'],
    ALL_BUTTONS['TEN_MESSAGE_PSYCHOLOGISTS'],
    ALL_BUTTONS['DELETE_USER_MESSAGE_FOR_PSYCHOLOGISTS'],
    ALL_BUTTONS['SEARCH_CATEGORY'],
    ALL_BUTTONS['NEW_CATEGORY'],
]
# Доступные действия для пользователя
buttons_available_action_user = [
    ALL_BUTTONS['SEND_MESSAGE_PSYCHOLOGISTS'],
    ALL_BUTTONS['SEARCH_CATEGORY'],
]
