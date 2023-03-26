import type { NarrowedContext, Scenes, Telegraf } from 'telegraf'
import type { Update, Message } from 'telegraf/typings/core/types/typegram'
import ANSWER_BOT from '../answerBot/index.json' assert { type: 'json' }
import db from '../utils/database.js'
import { ListCommands, ListPrivateCommands } from './enum.js'
import { COMMANDS } from './commands.js'
import { ListActions } from '../actions/enum.js'
import { getListInlineKeyboard } from '../utils/getListInlineKeyboard.js'

// Запуск чата
const start = async (ctx: Ctx) => {
  const { chat } = ctx
  const { type } = chat

  if (type === 'private') {
    await db.addNewChat(chat)
  }

  await ctx.replyWithSticker({
    url: ANSWER_BOT.start_sticky,
  })

  setTimeout(() => {
    const inlineKeyboard = getListInlineKeyboard(ListActions.START)

    return ctx.reply(ANSWER_BOT.select_category_all, inlineKeyboard)
  }, 2000)

  return ctx.reply(ANSWER_BOT.start)
}
// Помощь с ботом
const help = (ctx: Ctx) => {
  ctx.reply('Тут будет Помощь с ботом ...')
}
// Информация о боте
const info = (ctx: Ctx) => {
  ctx.reply('Тут будет Информация о боте ...')
}
// Выйти из чата
const quit = (ctx: Ctx) => {
  ctx.reply('Тут будет Выйти из чата ...')
}
// Получить все команды для психолога
const getAllCommandsPsychology = async (ctx: Ctx) => {
  try {
    const { chat } = ctx
    const isPsychologist = await db.checkIsPsychologist(chat.id)

    if (isPsychologist) {
      const inlineKeyboard = getListInlineKeyboard(ListActions.ALL_COMMANDS_PSYCHOLOGY)

      return await ctx.reply(ANSWER_BOT.all_commands_psychology, inlineKeyboard)
    } else {
      throw new Error('Доступ запрещен')
    }
  } catch (error) {
    console.log(error)
    return ctx.reply('Доступ запрещен...')
  }
}

const middlewareCommandsInit = (bot: Telegraf<Scenes.SceneContext<Scenes.SceneSessionData>>) => {
  const middlewareCommands: CallbackCommands = {
    [ListCommands.START]: start,
    [ListCommands.HELP]: help,
    [ListCommands.INFO]: info,
    [ListCommands.QUIT]: quit,
    [ListPrivateCommands.GET_ALL_COMMANDS_PSYCHOLOGY]: getAllCommandsPsychology,
  }

  for (const key in middlewareCommands) {
    if (Object.prototype.hasOwnProperty.call(middlewareCommands, key)) {
      bot.command(key, middlewareCommands[key as keyof typeof middlewareCommands])
    }
  }
}

// Установка и регистрация команд бота
export const commandsInit = async (bot: Telegraf<Scenes.SceneContext<Scenes.SceneSessionData>>) => {
  try {
    await bot.telegram.setMyCommands(COMMANDS)
    middlewareCommandsInit(bot)
  } catch (error) {
    console.log('Error COMMANDS', error)
  }
}

type CallbackCommands = Record<ListCommands & ListPrivateCommands, (ctx: Ctx) => void>
type Ctx = NarrowedContext<
  Scenes.SceneContext<Scenes.SceneSessionData>,
  {
    message: Update.New & Update.NonChannel & Message.TextMessage
    update_id: number
  }
>
