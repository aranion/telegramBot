import { ListActions } from '../actions/enum.js'

export const buttonActions: ButtonActions = {
  [ListActions.START]: {
    name: 'Старт...',
    subButtonActions: [ListActions.BEGIN, ListActions.SEND_MESSAGE_PSYCHOLOGY],
  },
  [ListActions.BEGIN]: {
    name: 'Выбрать категорию',
    subButtonActions: [ListActions.FAMILY, ListActions.SCHOOL, ListActions.FRIENDS],
  },
  [ListActions.SEND_MESSAGE_PSYCHOLOGY]: {
    name: 'Написать психологу',
  },
  [ListActions.CANCEL_MESSAGE_PSYCHOLOGY]: {
    name: 'Отменить',
  },
  [ListActions.GET_ALL_MESSAGES_PSYCHOLOGY]: {
    name: 'Получить все сообщения для психолога',
  },
  [ListActions.DELETE_MESSAGE_PSYCHOLOGY]: {
    name: 'Удалить указанное сообщение',
  },
  [ListActions.ALL_COMMANDS_PSYCHOLOGY]: {
    name: 'Все команды доступные психологу',
    subButtonActions: [ListActions.GET_ALL_MESSAGES_PSYCHOLOGY, ListActions.DELETE_MESSAGE_PSYCHOLOGY],
  },
  [ListActions.FAMILY]: {
    name: 'Семья',
    subButtonActions: [ListActions.FAMILY_PARENTS, ListActions.FAMILY_BROTHER_SISTER],
  },
  [ListActions.SCHOOL]: {
    name: 'Школа',
    subButtonActions: [ListActions.SCHOOL_BULLYING],
  },
  [ListActions.FRIENDS]: {
    name: 'Друзья',
  },
  [ListActions.FAMILY_PARENTS]: {
    name: 'Конфликт с родителями',
  },
  [ListActions.FAMILY_BROTHER_SISTER]: {
    name: 'Конфликт с братом/сестрой',
  },
  [ListActions.SCHOOL_BULLYING]: {
    name: 'Буллинг',
  },
  [ListActions.HELP]: {
    name: 'Буллинг',
  },
}

type ButtonActions = Record<ListActions, Button>
type Button = {
  name: string
  subButtonActions?: ListActions[]
}

// {
//   action: ListActions.LIKE,
//   name: '👍',
// },
// {
//   action: ListActions.DISLIKE,
//   name: '👎',
// },
