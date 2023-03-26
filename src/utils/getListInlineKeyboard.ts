import { Markup } from 'telegraf'
import { ListActions } from '../actions/enum.js'
import { buttonActions } from '../constants/buttonActions.js'

// Получить список кнопок из buttonActions
export const getListInlineKeyboard = (action: keyof typeof ListActions) => {
  const subButtonActions = buttonActions[ListActions[action]].subButtonActions

  // Вернуть вложенные кнопки если они есть
  if (subButtonActions) {
    return Markup.inlineKeyboard(
      subButtonActions.map(button => [Markup.button.callback(buttonActions[button].name, button)]),
    )
  } else {
    // Вернуть одну кнопку если вложенных кнопок нет
    return Markup.inlineKeyboard([
      Markup.button.callback(buttonActions[ListActions[action]].name, ListActions[action]),
    ])
  }
}
