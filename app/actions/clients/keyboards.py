from telebot import types

from app.constants.text import TextBtn
from app.constants.handlers import HandlerNames
from app.requests.models import GetClientsReqDto

Handlers = HandlerNames()


def clients_actions_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    add = types.KeyboardButton(text=TextBtn.ADD_CLIENT)
    find = types.KeyboardButton(text=TextBtn.ALL_CLIENTS)
    import_clients = types.KeyboardButton(text=TextBtn.IMPORT_CLIENTS)
    main_menu = types.KeyboardButton(text=TextBtn.MAIN_MENU)

    keyboard.add(add, find, import_clients, main_menu)
    return keyboard


def client_keyboard(uid):
    keyboard = types.InlineKeyboardMarkup()

    edit = types.InlineKeyboardButton(text=TextBtn.EDIT, callback_data=Handlers.CLIENT_UPDATE(uid))
    remove = types.InlineKeyboardButton(text=TextBtn.REMOVE, callback_data=Handlers.CLIENT_REMOVE(uid))

    keyboard.row(edit, remove)

    return keyboard


def show_clients_keyboard(response: GetClientsReqDto):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for client in response['data']:
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{client['last_name']} {client['first_name']} {client['patronymic'] or ''}",
                callback_data=Handlers.CLIENT_GET(client['id']))
        )

    page = response['meta']['page']
    pages_count = response['meta']['pageCount']
    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1

    if pages_count > 1:
        left_button = types.InlineKeyboardButton("←", callback_data=Handlers.CLIENT_PAGINATION_LEFT(left))
        page_button = types.InlineKeyboardButton(f"{page}/{pages_count}", callback_data="_")
        right_button = types.InlineKeyboardButton("→", callback_data=Handlers.CLIENT_PAGINATION_RIGHT(right))

        keyboard.row(left_button, page_button, right_button)

    # keyboard.add(types.InlineKeyboardButton("Закрыть", callback_data="client_all_data_close"))

    return keyboard


def show_client_get_data_keyboard(uid, page=1):
    keyboard = types.InlineKeyboardMarkup()

    edit = types.InlineKeyboardButton(text=TextBtn.EDIT, callback_data=Handlers.CLIENT_UPDATE(uid))
    remove = types.InlineKeyboardButton(text=TextBtn.REMOVE, callback_data=Handlers.CLIENT_REMOVE(uid))

    # TODO: запомнить номер страницы при возврате
    back = types.InlineKeyboardButton(text=TextBtn.BACK, callback_data=Handlers.BACK_TO_ALL_CLIENTS(page))

    keyboard.row(edit, remove)
    keyboard.row(back)

    return keyboard


def add_client_cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    cancel = types.KeyboardButton(text=TextBtn.CANCEL_ADD_CLIENT)
    keyboard.add(cancel)

    return keyboard


def add_client_confirm_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    add = types.InlineKeyboardButton(text=TextBtn.ADD, callback_data=Handlers.CLIENT_ADD_STATE_TO_DB)
    repeat = types.InlineKeyboardButton(text=TextBtn.AGAIN, callback_data=Handlers.CLIENT_EDIT_STATE)

    keyboard.add(add, repeat)

    return keyboard


def add_client_reply_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    repeat = types.InlineKeyboardButton(text=TextBtn.REPEAT, callback_data=Handlers.CLIENT_ADD_STATE_TO_DB)
    cancel = types.InlineKeyboardButton(text=TextBtn.CANCEL, callback_data=Handlers.CLIENT_CANCEL_ADD_STATE_TO_DB)

    keyboard.add(repeat, cancel)

    return keyboard


def add_client_patronymic_is_true_or_none():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    patronymic_in_none = types.KeyboardButton(text=TextBtn.PATRONYMIC_IS_NONE)
    cancel = types.KeyboardButton(text=TextBtn.CANCEL_ADD_CLIENT)

    keyboard.add(patronymic_in_none, cancel)

    return keyboard


def add_client_about_is_none():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    about_in_none = types.KeyboardButton(text=TextBtn.ABOUT_IS_NONE)
    cancel = types.KeyboardButton(text=TextBtn.CANCEL_ADD_CLIENT)

    keyboard.add(about_in_none, cancel)

    return keyboard
