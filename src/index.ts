import { Telegraf, Scenes, Markup } from 'telegraf'
import type { InlineQueryResult } from 'telegraf/typings/core/types/typegram.js'
import { config } from './config'
// import fileQ from './questions/index.json' assert { type: 'json' };
// import db from './utils/database.js';

const bot = new Telegraf<Scenes.SceneContext>(config.botToken)

const COMMANDS = [
  { command: '/start', description: 'Запуск бота' },
  {
    command: '/info',
    description: 'Тест функционала',
  },
  {
    command: '/help',
    description: 'Показать справку',
  },
  {
    command: '/quit',
    description: 'Выйти из чата',
  },
  {
    command: '/oldschool',
    description: 'oldschool',
  },
  {
    command: '/hipster',
    description: 'hipster',
  },
  {
    command: '/game',
    description: 'Game',
  },
]

const chats: Record<string, number> = {}

const init = (): void => {
  bot.telegram.setMyCommands(COMMANDS)

  bot.start(ctx => ctx.reply('Welcome'))
  bot.help(ctx => ctx.reply('Send me a sticker'))
  bot.command('oldschool', ctx => ctx.reply('Hello'))
  bot.command('hipster', Telegraf.reply('λ'))

  bot.action('like', ctx => {
    return ctx.answerCbQuery('like!')
  })

  bot.action('dislike', ctx => {
    return ctx.answerCbQuery('dislike!')
  })

  bot.action(/.+/, ctx => {
    return ctx.answerCbQuery(`Ой, ${ctx.match[0]}! нет такого`)
  })

  bot.use(async (ctx, next) => {
    // МИДЛЕВАРА
    console.time(`Processing update ${ctx.update.update_id}`)
    await next()
    console.timeEnd(`Processing update ${ctx.update.update_id}`)
  })

  bot.on('callback_query', async ctx => {
    console.log('callback_query')
    await ctx.telegram.answerCbQuery(ctx.callbackQuery.id)
    await ctx.answerCbQuery()
  })

  bot.on('inline_query', async ctx => {
    console.log('inline_query')
    const result: InlineQueryResult[] = []
    await ctx.telegram.answerInlineQuery(ctx.inlineQuery.id, result)
    await ctx.answerInlineQuery(result)
  })

  bot.on('text', async ctx => {
    const { update, chat } = ctx
    const { message } = update
    const { text } = message
    console.log('ctx', message.text)

    await ctx.reply('Ищу ответ...')

    if (text.toLocaleLowerCase() === 'нина') {
      await ctx.replyWithSticker({
        url: 'https://chpic.su/_data/stickers/b/Belkosemja/Belkosemja_011.webp',
      })
      return ctx.reply('Пошли спать!')
    }
    if (text === '/start') {
      await ctx.replyWithSticker({
        url: 'https://chpic.su/_data/stickers/b/Belkosemja/Belkosemja_011.webp',
      })
      return ctx.reply(
        `Привет! Меня зовут Марвин. Я – интеллектуальная система, которая постарается 
        помочь тебе решить твои проблемы. Ты можешь рассказать мне о своей проблеме, 
        пообщаться со мной или послушать мой совет.`,
      )
    }

    if (text === '/info') {
      return ctx.reply('Тебя зовут: ' + ('first_name' in chat && chat.first_name))
    }

    if (text === '/game') {
      await ctx.reply('Загадал цифру от 0 до 9, нужно отгадать.')
      const random = Math.floor(Math.random() * 10)

      chats[chat.id] = random

      bot.action('test', async ctx => {
        console.log(ctx)
        try {
          await ctx.answerCbQuery()
        } catch (error) {
          console.error(error)
        }
      })

      return ctx.reply(
        'Можно отгадывать',
        Markup.inlineKeyboard([
          Markup.button.callback('👍', 'like'),
          Markup.button.callback('👎', 'dislike'),
          Markup.button.callback('0', '0'),
          Markup.button.callback('1', '1'),
          Markup.button.callback('2', '2'),
          Markup.button.callback('3', '3'),
          Markup.button.callback('4', '4'),
          Markup.button.callback('5', '5'),
          Markup.button.callback('6', '6'),
          Markup.button.callback('7', '7'),
          Markup.button.callback('8', '8'),
          Markup.button.callback('9', '9'),
        ]),
      )
    }

    return ctx.reply('Что-то я Вас не понимаю...')
  })
  // bot.on('text', (ctx) => {
  //   console.log(ctx.update.message);

  //   // db.writeMessage(ctx.update.message.text, ctx.update.message.date);
  //   console.log(ctx);

  //   const res = fileQ.data.find((item) => {
  //     console.log(item.question, '===', ctx.update.message.text);

  //     if (
  //       // typeof ctx.update.message === 'string' &&
  //       item.question === ctx.update.message.text
  //     ) {
  //       return true;
  //     }
  //     return false;
  //   });

  //   if (res?.response) {
  //     ctx.reply(res.response);
  //   } else {
  //     ctx.reply(fileQ.data[fileQ.data.length - 1].response);
  //   }
  //   // ctx.reply(
  //   //   'Привет! Меня зовут Марвин. Я – интеллектуальная система,'
  //   // );
  // });

  bot.launch()
}

init()

process.once('SIGINT', () => {
  bot.stop('SIGINT')
})
process.once('SIGTERM', () => {
  bot.stop('SIGTERM')
})
