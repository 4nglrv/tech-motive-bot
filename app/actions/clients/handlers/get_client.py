from app.actions.clients.keyboards import clients_actions_keyboard, show_clients_keyboard, client_keyboard, show_client_get_data_keyboard

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
from app.actions.clients.handlers.add_client import client_state_start_handler
from app.actions.start.handlers import start_handler
from app.constants.text import TextMsg, TextBtn
from app.constants.handlers import HandlerNames
from app.requests.api import API

Handlers = HandlerNames()


async def error_handler(chat_id: int, error: Exception, bot: AsyncTeleBot):
    await bot.send_message(chat_id, text=TextMsg.UNKNOWN_ERROR(error))


async def clients_handler(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, TextMsg.SELECT_CLIENT_ACTION, reply_markup=clients_actions_keyboard())


async def clients_get_all_handler(message: Message, bot: AsyncTeleBot, page=1, edit_message=False):
    api = API(bot, message.chat.id)
    response = await api.get_clients(page)

    if len(response['data']) > 0:
        if edit_message:
            # значит переключаемся между страничками
            await bot.edit_message_text(
                text=TextMsg.CLIENTS_IN_DATABASE,
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=show_clients_keyboard(response),
            )
        else:
            # иначе просто отправляем сообщюху
            await bot.send_message(
                text=TextMsg.CLIENTS_IN_DATABASE,
                chat_id=message.chat.id,
                reply_markup=show_clients_keyboard(response)
            )
    else:
        # ну или пользователя создайте хотябы
        await bot.send_message(
            chat_id=message.chat.id,
            text=TextMsg.ADD_FIRST_CLIENT
        )


async def show_client_handler(message: Message, bot: AsyncTeleBot):
    api = API(bot, chat_id=message.chat.id)
    response = await api.get_client_by_phone(message.text)

    if response:
        await bot.send_message(
            chat_id=message.chat.id,
            text=TextMsg.CLIENT_FOUND(response),
            parse_mode='Markdown',
            reply_markup=client_keyboard(response['id'])
        )


async def clients_get_callback_handler(callback: CallbackQuery, bot: AsyncTeleBot):
    chat_id = callback.message.chat.id
    message_id = callback.message.id

    api = API(bot, chat_id)

    if Handlers.CLIENT_GET() in callback.data:
        uid = callback.data.replace(Handlers.CLIENT_GET(), '')

        client_data = await api.get_client_by_id(uid)
        await bot.edit_message_text(
            text=TextMsg.CLIENT_INFO(client_data),
            chat_id=str(chat_id),
            message_id=message_id,
            reply_markup=show_client_get_data_keyboard(uid),
            parse_mode='Markdown'
        )

    if Handlers.CLIENT_UPDATE() in callback.data:
        uid = callback.data.replace(Handlers.CLIENT_UPDATE(), '')
        await bot.send_message(chat_id, f'Тут мы будем обновлять инфу о пользователе с id {uid}')

    if Handlers.CLIENT_REMOVE() in callback.data:
        uid = callback.data.replace(Handlers.CLIENT_REMOVE(), '')
        await bot.send_message(chat_id, f'Тут мы будем удалять инфу о пользователе с id {uid}')

    if Handlers.CLIENT_PAGINATION_LEFT() in callback.data:
        page = callback.data.replace(Handlers.CLIENT_PAGINATION_LEFT(), '')
        await clients_get_all_handler(callback.message, bot, page=int(page), edit_message=True)

    if Handlers.CLIENT_PAGINATION_RIGHT() in callback.data:
        page = callback.data.replace(Handlers.CLIENT_PAGINATION_RIGHT(), '')
        await clients_get_all_handler(callback.message, bot, page=int(page), edit_message=True)

    if Handlers.BACK_TO_ALL_CLIENTS() in callback.data:
        page = callback.data.replace(Handlers.BACK_TO_ALL_CLIENTS(), '')
        await clients_get_all_handler(callback.message, bot, page=int(page), edit_message=True)

    if Handlers.ALL_CLIENTS in callback.data:
        await clients_get_all_handler(callback.message, bot, edit_message=True)


def register_get_client_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(clients_handler, regexp=TextBtn.CLIENTS, pass_bot=True)
    bot.register_message_handler(client_state_start_handler, regexp=TextBtn.ADD_CLIENT, pass_bot=True)
    bot.register_message_handler(clients_get_all_handler, regexp=TextBtn.ALL_CLIENTS, pass_bot=True)
    bot.register_message_handler(start_handler, regexp=TextBtn.MAIN_MENU, pass_bot=True)

    bot.register_callback_query_handler(
        clients_get_callback_handler,
        pass_bot=True, func=lambda callback: True if Handlers.GET_CLIENT_PREFIX in callback.data else False
    )
