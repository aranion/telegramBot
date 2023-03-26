import type { Scenes, Telegraf } from 'telegraf'
import type { CallbackQuery } from 'telegraf/typings/core/types/typegram.js'
import ANSWER_BOT from '../answerBot/index.json' assert { type: 'json' }
import db from '../utils/database.js'
import { buttonActions } from '../constants/buttonActions.js'
import { ListActions } from './enum.js'
import { getListInlineKeyboard } from '../utils/getListInlineKeyboard.js'

// Действия при нажатии на кнопки
export const actionsInit = (bot: Telegraf<Scenes.SceneContext<Scenes.SceneSessionData>>) => {
  try {
    // Действие "Написать психологу"
    bot.action(ListActions.SEND_MESSAGE_PSYCHOLOGY, async ctx => {
      const chatId = ctx.chat?.id

      if (chatId) {
        const idTimeoutNextMessagePsychology = await db.getIdNextMessagePsychology(chatId)
        const inlineKeyboard = getListInlineKeyboard(ListActions.CANCEL_MESSAGE_PSYCHOLOGY)

        if (idTimeoutNextMessagePsychology) {
          clearTimeout(idTimeoutNextMessagePsychology)
        }

        const idTimeout = setTimeout(async () => {
          const inlineKeyboard = getListInlineKeyboard(ListActions.START)

          await db.setIdNextMessagePsychology(chatId, null)
          await ctx.reply(ANSWER_BOT.next_message_psychology_end, inlineKeyboard)
        }, 5000) //TODO: Нужно заменить на 1800000)

        await db.setIdNextMessagePsychology(ctx.chat.id, idTimeout)

        return ctx.reply(ANSWER_BOT.next_message_psychology, inlineKeyboard)
      } else {
        return ctx.answerCbQuery(ANSWER_BOT.error)
      }
    })
    // Кнопка "Получить все сообщения для психолога"
    bot.action(ListActions.GET_ALL_MESSAGES_PSYCHOLOGY, async ctx => {
      const chatId = ctx.chat?.id

      if (chatId) {
        const isPsychologist = await db.checkIsPsychologist(ctx.chat?.id)

        if (isPsychologist) {
          const messagesPsychology = await db.getMessagesPsychology()

          if (messagesPsychology) {
            let index = 1

            for (const key in messagesPsychology) {
              if (Object.prototype.hasOwnProperty.call(messagesPsychology, key)) {
                // Показать только первые 10 сообщений
                if (index > 10) {
                  return ctx.reply(ANSWER_BOT.show_first_10_message)
                }
                await ctx.reply(`Id: ${key}, Сообщение: "${messagesPsychology[key].text}"`)
              }
              index++
            }
            // Показать все сообщения, если их не больше 10
            return ctx.reply(ANSWER_BOT.show_all_message)
          } else {
            return ctx.reply(ANSWER_BOT.not_messages)
          }
        } else {
          return ctx.reply(ANSWER_BOT.not_access)
        }
      } else {
        return ctx.reply(ANSWER_BOT.empty_chat_id)
      }
    })
    // При нажатии "Отменить" при отправке сообщение психологу
    bot.action(ListActions.CANCEL_MESSAGE_PSYCHOLOGY, async ctx => {
      const chatId = ctx.chat?.id

      if (chatId) {
        const idTimeoutNextMessagePsychology = await db.getIdNextMessagePsychology(chatId)
        const inlineKeyboard = getListInlineKeyboard(ListActions.START)

        if (idTimeoutNextMessagePsychology) {
          clearTimeout(idTimeoutNextMessagePsychology)
          await ctx.reply(ANSWER_BOT.cancel_message_psychology, inlineKeyboard)
        }

        return null
      } else {
        return ctx.reply(ANSWER_BOT.empty_chat_id)
      }
    })
    // Сработает на любые кнопки
    bot.action(/.+/, ctx => {
      const callback_query = ctx.update.callback_query

      if ('data' in callback_query) {
        const { data } = callback_query as CallbackQuery & { data: keyof typeof ListActions }
        const action = buttonActions[ListActions[data]]

        if (!action) {
          return ctx.answerCbQuery(`Я не знаю такого действия ${ctx.match[0]}!`)
        }

        if (!action?.subButtonActions) {
          return ctx.reply('Находится в разработке!')
        }

        const inlineKeyboard = getListInlineKeyboard(ListActions[data])

        return ctx.reply(ANSWER_BOT.select_category, inlineKeyboard)
      }

      return ctx.answerCbQuery(`Ой, ${ctx.match[0]}! нет такой`)
    })
  } catch (error) {
    console.log('Error ACTION', error)
  }
}
