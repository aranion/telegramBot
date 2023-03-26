import { initializeApp } from 'firebase/app'
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth'
import { Database as DatabaseType, getDatabase, ref, set, get } from 'firebase/database'
import { config } from '../config.js'
import type { FirebaseApp } from 'firebase/app'
import type { Chat, Update, Message } from 'telegraf/typings/core/types/typegram.js'
import type { PsychologyMessage, UserChat, UserMessage } from '../types/index.js'

class Database {
  private db: DatabaseType | null = null
  private app: FirebaseApp | null = null

  constructor() {
    try {
      this.app = initializeApp({ ...config.firebase })

      const auth = getAuth()
      const { email, password } = config.authorFirebase

      signInWithEmailAndPassword(auth, email, password)

      this.db = getDatabase(this.app)
    } catch (error) {
      console.error('Ошибка инициализации database', error)
    }
  }

  get getDB() {
    return this.db as DatabaseType
  }

  // Создать новый чат, если он не создан
  public async addNewChat(chat: Chat.PrivateChat) {
    const { id } = chat
    const refPath = ref(this.getDB, `chats/${id}`)

    get(refPath)
      .then(res => {
        if (!res.exists()) {
          set(refPath, {
            ...chat,
            idTimeoutNextMessagePsychology: 'null',
          }).catch(console.error)
        }
      })
      .catch(this.error)
  }

  // Проверить есть ли у пользователя права психолога
  public async checkIsPsychologist(chatId: number) {
    const refPath = ref(this.getDB, `chats/${chatId}/isPsychologist`)

    return get(refPath)
      .then<boolean>(res => {
        if (res.exists()) {
          return res.val()
        }
        return false
      })
      .catch(this.error)
  }

  // Получить данные чата по id чата
  public async getChatById(chatId: number) {
    const refPath = ref(this.getDB, `chats/${chatId}`)

    return get(refPath)
      .then<UserChat>(res => {
        if (res.exists()) {
          return res.val()
        }
        return null
      })
      .catch(this.error)
  }

  // Получить id психолога
  public async getIdPsychologist() {
    const refPath = ref(this.getDB, 'chats')

    return get(refPath)
      .then<number | null>(res => {
        if (res.exists()) {
          const chats = res.val() as Record<number, UserChat>

          for (const key in chats) {
            if (Object.prototype.hasOwnProperty.call(chats, key)) {
              const { isPsychologist, id } = chats[key]

              if (isPsychologist) {
                return +id
              }
            }
          }
        }
        return null
      })
      .catch(this.error)
  }

  // Получить все сообщения в чате по id чата
  public async getMessagesByChatId(chatId: number) {
    const refPath = ref(this.getDB, `chats/${chatId}/messages`)

    return get(refPath)
      .then<UserMessage[] | null>(res => {
        if (res.exists()) {
          return res.val()
        }
        return null
      })
      .catch(this.error)
  }

  // Получить id таймера для отмены перенаправления сообщения психологу
  public async getIdNextMessagePsychology(chatId: number) {
    const refPath = ref(this.getDB, `chats/${chatId}/idTimeoutNextMessagePsychology`)

    return get(refPath)
      .then<NodeJS.Timeout | null>(res => {
        if (res.val() !== 'null') {
          return res.val()
        }
        return null
      })
      .catch(this.error)
  }

  // Получить все сообщения для психолога
  public async getMessagesPsychology() {
    const refPath = ref(this.getDB, 'messagesPsychology')

    return get(refPath)
      .then<Record<number, PsychologyMessage>>(res => {
        if (res.exists()) {
          return res.val()
        }
        return null
      })
      .catch(this.error)
  }

  // Получить сообщение для психолога по id сообщения
  public async getMessagePsychologyById(idMessage: number) {
    const refPath = ref(this.getDB, `messagesPsychology/${idMessage}`)

    return get(refPath)
      .then<PsychologyMessage>(res => {
        if (res.exists()) {
          return res.val()
        }
        return null
      })
      .catch(this.error)
  }

  // Записать в БД сообщение чата
  public async setMessage(message: Update.New & Update.NonChannel & Message.TextMessage) {
    const { date, message_id, text, chat } = message
    const chatId = chat.id
    const refPath = ref(this.getDB, `chats/${chatId}/messages`)
    const newMessage: UserMessage = { date, message_id, text }

    this.getMessagesByChatId(chatId)
      .then(res => {
        const maxListMessagesDB = 4
        const setMessages = (listMsg: UserMessage[]) => {
          set(refPath, listMsg).catch(this.error)
        }

        if (res) {
          if (res.length > maxListMessagesDB) {
            setMessages([...res.slice(0, maxListMessagesDB), newMessage])
          } else {
            setMessages([...res, newMessage])
          }
        } else {
          setMessages([newMessage])
        }
      })
      .catch(this.error)
  }

  // Записать id таймера для отмены перенаправления сообщения психологу
  public async setIdNextMessagePsychology(
    chatId: number,
    idTimeoutNextMessagePsychology: NodeJS.Timeout | null,
  ) {
    const refPath = ref(this.getDB, `chats/${chatId}/idTimeoutNextMessagePsychology`)
    const value = idTimeoutNextMessagePsychology === null ? 'null' : Number(idTimeoutNextMessagePsychology)

    await set(refPath, value).catch(this.error)
  }

  // Записать сообщение для психолога
  public async setMessagePsychology(messages: Update.New & Update.NonChannel & Message.TextMessage) {
    const refPath = ref(this.getDB, 'messagesPsychology')
    const { message_id, chat, date, text } = messages
    const newMessage: PsychologyMessage = { chat, date, text }

    this.getMessagesPsychology()
      .then(res => {
        set(refPath, { ...res, [message_id]: newMessage }).catch(this.error)
      })
      .then(() => {
        if ('chat' in messages) {
          const chat = messages.chat as Chat.PrivateChat
          this.setIdNextMessagePsychology(chat.id, null)
        }
      })
      .catch(this.error)
  }

  // Удалить сообщение для психолога по id сообщения
  public async deleteMessagePsychologyById(idMessage: number) {
    const refPath = ref(this.getDB, 'messagesPsychology')

    this.getMessagesPsychology()
      .then(res => {
        if (res) {
          delete res[idMessage]
          set(refPath, res).catch(this.error)
        }
      })
      .catch(this.error)
  }

  // Вывод ошибок
  private error(err: Error) {
    console.error(err)
    return null
  }
}

const db = new Database()

export default db
