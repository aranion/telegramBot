import type { InlineQueryResult } from 'telegraf/typings/core/types/typegram.js'
import ANSWER_BOT from './answerBot/index.json' assert { type: 'json' }
import db from './utils/database.js'
import { Scenes, Telegraf } from 'telegraf'
import { config } from './config.js'
import { actionsInit } from './actions/index.js'
import { commandsInit } from './commands/index.js'
import { getListInlineKeyboard } from './utils/getListInlineKeyboard.js'
import { ListActions } from './actions/enum.js'

const bot = new Telegraf<Scenes.SceneContext>(config.botToken)

const init = (): void => {
  actionsInit(bot)
  commandsInit(bot)
  // bot.use(async (ctx, next) => {
  //   console.time(`Processing update ${ctx.update.update_id}`)
  //   await next()
  //   console.timeEnd(`Processing update ${ctx.update.update_id}`)
  // })
  // bot.use((ctx, next) => {
  //   // Дополнительная переменная
  //   ctx.myProp = ctx.chat?.first_name?.toUpperCase();
  //   return next();
  // });

  // Приветствие для психолога
  bot.telegram
    .sendMessage(
      854241396,
      `Привет! Я снова онлайн! :)
       Вот тут написано что я могу`,
      getListInlineKeyboard(ListActions.GET_ALL_MESSAGES_PSYCHOLOGY),
    )
    .then(res => {
      console.log('Бот онлайн', res)
    })

  bot.on('callback_query', async ctx => {
    await ctx.telegram.answerCbQuery(ctx.callbackQuery.id)
    return ctx.answerCbQuery()
  })

  bot.on('inline_query', async ctx => {
    const result: InlineQueryResult[] = []
    await ctx.telegram.answerInlineQuery(ctx.inlineQuery.id, result)
    return ctx.answerInlineQuery(result)
  })

  bot.on('text', async ctx => {
    try {
      const { chat } = ctx
      const idTimeoutNextMessagePsychology = await db.getIdNextMessagePsychology(chat.id)
      const newMessage = ctx.update.message

      // Записать все сообщения в БД чата пользователя
      await db.setMessage(newMessage)

      // Очистить id таймаута и отправить уведомление психологу о новом сообщении
      if (idTimeoutNextMessagePsychology) {
        const idPsychology = await db.getIdPsychologist()
        const { message } = ctx
        const { text, message_id } = message
        const newUserMessage = `id: ${message_id}, сообщение: "${text}"`

        clearTimeout(idTimeoutNextMessagePsychology)

        // Поместить сообщение в список всех сообщений для психолога
        await db.setMessagePsychology(message)

        // Отправить поступившее сообщение с вопросом в чат психолога
        if (idPsychology) {
          await ctx.telegram.sendMessage(idPsychology, ANSWER_BOT.new_message_received)
          await ctx.telegram.sendMessage(idPsychology, newUserMessage)
        }
        return await ctx.reply(ANSWER_BOT.send_message_psychology)
      }

      const isPsychology = await db.checkIsPsychologist(chat.id)

      // Если сообщение от психолога, проверяется наличие id сообщения в ответе психолога для ответа
      if (isPsychology) {
        const msg = newMessage.text.trim().split(' ')
        const idMessage = Number(msg[0])
        const answerPsychologyString = msg.slice(1).join(' ')

        if (!isNaN(idMessage)) {
          const messagePsychology = await db.getMessagePsychologyById(idMessage)

          if (messagePsychology) {
            const { chat, text } = messagePsychology

            await ctx.telegram.sendMessage(chat.id, 'Вы ранее направляли вопрос психологу')
            await ctx.telegram.sendMessage(chat.id, `Вопрос: "${text}"`)
            await ctx.telegram.sendMessage(chat.id, `Ответ: "${answerPsychologyString}"`)
            await db.deleteMessagePsychologyById(idMessage)
            return await ctx.reply(ANSWER_BOT.successfully_sent)
          }
        } else {
          const inlineKeyboard = getListInlineKeyboard(ListActions.GET_ALL_MESSAGES_PSYCHOLOGY)

          return await ctx.reply(ANSWER_BOT.error_message_id_in_answer_psychology, inlineKeyboard)
        }
      }
      // setTimeout(() => {
      //   ctx.update.message.chat.id //854241396
      //   ctx.sendMessage('Ответ на вопрос')
      // }, 10000)

      // const id = setTimeout(() => {
      //   ctx.reply(ANSWER_BOT.search)
      // }, 3000)

      // clearTimeout(id)
      return await ctx.reply(ANSWER_BOT.no_understand)
    } catch (error) {
      return ctx.answerCbQuery(ANSWER_BOT.error)
    }
  })

  bot.launch()
}

init()

process.once('SIGINT', () => {
  bot.stop('SIGINT')
})
process.once('SIGTERM', () => {
  bot.stop('SIGTERM')
})
