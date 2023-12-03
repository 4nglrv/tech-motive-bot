from telebot import types

from app.constants.text import TextBtn


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    Clients = types.KeyboardButton(text=TextBtn.CLIENTS)
    Orders = types.KeyboardButton(text=TextBtn.ORDERS)

    keyboard.add(Clients, Orders)
    return keyboard
