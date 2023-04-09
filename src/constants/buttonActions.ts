import { ListActions } from '../actions/enum.js'

export const buttonActions: ButtonActions = {
  [ListActions.START]: {
    name: 'Старт...',
    subButtonActions: [ListActions.BEGIN, ListActions.SEND_MESSAGE_PSYCHOLOGY],
  },
  [ListActions.BEGIN]: {
    name: 'Выбрать категорию',
    subButtonActions: [ListActions.CTG_FAMILY, ListActions.CTG_SCHOOL, ListActions.CTG_FRIENDS],
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

  [ListActions.CTG_FAMILY]: {
    name: 'Семья',
    subButtonActions: [ListActions.CTG_FAMILY_PARENTS, ListActions.CTG_FAMILY_BROTHER_SISTER],
  },
  [ListActions.CTG_SCHOOL]: {
    name: 'Школа',
    subButtonActions: [ListActions.CTG_SCHOOL_BULLYING],
  },
  [ListActions.CTG_FRIENDS]: {
    name: 'Друзья',
  },
  [ListActions.CTG_FAMILY_PARENTS]: {
    name: 'Конфликт с родителями',
  },
  [ListActions.CTG_FAMILY_BROTHER_SISTER]: {
    name: 'Конфликт с братом/сестрой',
  },
  [ListActions.CTG_SCHOOL_BULLYING]: {
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
