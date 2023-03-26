import type { Update, Message, Chat } from 'telegraf/typings/core/types/typegram'

export type UserChat = Chat.PrivateChat & {
  messages?: UserMessage[] | null
  isPsychologist?: boolean
  idTimeoutNextMessagePsychology: NodeJS.Timeout | null
}

export type UserMessage = Omit<Update.New & Update.NonChannel & Message.TextMessage, 'chat' | 'from'>
export type PsychologyMessage = Omit<
  Update.New & Update.NonChannel & Message.TextMessage,
  'from' | 'message_id'
>
