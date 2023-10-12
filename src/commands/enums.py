import enum


class ListCommands(enum.Enum):
    START = 'start',
    INFO = 'info',
    HELP = 'help',


class ListPrivateCommands(enum.Enum):
    GET_ALL_COMMANDS_PSYCHOLOGISTS = 'all_cmd',
