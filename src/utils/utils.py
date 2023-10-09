from telebot import types


def generateReplyMarkup(list_data_buttons, cols=1):
    """Возвращает подготовленные кнопки"""

    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        """Рассчитать элементы кнопок по столбикам"""
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    button_list = []

    for data_button in list_data_buttons:
        text = data_button.get('text')
        callback_data = ''.join(data_button.get('action'))
        button_list.append(types.InlineKeyboardButton(text, callback_data=callback_data))
    reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols=cols))

    return reply_markup
