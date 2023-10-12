from src.commands.enums import ListCommands, ListPrivateCommands
from src.utils.utils import getValueEnum

COMMANDS = [
    {'command': getValueEnum('START', ListCommands), 'description': 'Запуск бота'},
    {'command': getValueEnum('INFO', ListCommands), 'description': 'Информация о боте'},
    {'command': getValueEnum('HELP', ListCommands), 'description': 'Помощь в работе с ботом'},
]

PRIVATE_COMMANDS = [
    {
        'command': getValueEnum('GET_ALL_COMMANDS_PSYCHOLOGISTS', ListPrivateCommands),
        'description': 'Получить все команды психолога'
    },
]
