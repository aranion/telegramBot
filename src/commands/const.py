from src.commands.enums import ListCommands, ListPrivateCommands

COMMANDS = [
    {'command': ListCommands.START.value, 'description': 'Запуск бота'},
    {'command': ListCommands.INFO.value, 'description': 'Информация о боте'},
    {'command': ListCommands.HELP.value, 'description': 'Помощь в работе с ботом'},
    {'command': ListCommands.QUIT.value, 'description': 'Выйти из чата'},
]

PRIVATE_COMMANDS = [
    {
        'command': ListPrivateCommands.GET_ALL_COMMANDS_PSYCHOLOGISTS.value,
        'description': 'Получить все команды психолога'
    },
]
