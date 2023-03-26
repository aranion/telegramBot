import { ListCommands, ListPrivateCommands } from './enum.js'

export const COMMANDS: Commands = [
  { command: ListCommands.START, description: 'Запуск бота' },
  { command: ListCommands.INFO, description: 'Информация о Боте' },
  { command: ListCommands.HELP, description: 'Помощь в работе с Ботом' },
  { command: ListCommands.QUIT, description: 'Выйти из чата' },
]

export const PRIVATE_COMMANDS: Commands = [
  { command: ListPrivateCommands.GET_ALL_COMMANDS_PSYCHOLOGY, description: 'Получить все команды психолога' },
]

type Commands = Array<{
  command: ListCommands | ListPrivateCommands
  description: string
}>
