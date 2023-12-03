from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from app.actions.clients.keyboards import add_client_confirm_keyboard, add_client_cancel_keyboard, \
    clients_actions_keyboard, add_client_patronymic_is_true_or_none, add_client_about_is_none
from app.constants.text import TextMsg, TextBtn
from app.constants.handlers import HandlerNames
from app.common.utils import is_phone
from app.requests.api import API

Handlers = HandlerNames()


class ClientState(StatesGroup):
    first_name = State()
    last_name = State()
    patronymic = State()
    city = State()
    address = State()
    phone = State()
    about_client = State()


async def client_state_cancel_handler(message: Message, bot: AsyncTeleBot):
    """
    Cancel state
    """
    await bot.delete_state(message.from_user.id, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.CANCELED, reply_markup=clients_actions_keyboard())


async def client_state_start_handler(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, ClientState.first_name, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.TYPE_FIRST_NAME, reply_markup=add_client_cancel_keyboard())


async def client_get_first_name_handler(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, ClientState.last_name, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.TYPE_LAST_NAME)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['first_name'] = message.text


async def client_get_last_name_handler(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, ClientState.patronymic, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.TYPE_PATRONYMIC, reply_markup=add_client_patronymic_is_true_or_none())

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['last_name'] = message.text


async def client_get_patronymic_handler(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, ClientState.city, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.TYPE_CITY, reply_markup=add_client_cancel_keyboard())

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if TextBtn.PATRONYMIC_IS_NONE in message.text:
            data['patronymic'] = None
        else:
            data['patronymic'] = message.text


async def client_get_city_handler(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, ClientState.address, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.TYPE_ADDRESS)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


async def client_get_address_handler(message: Message, bot: AsyncTeleBot):
    await bot.set_state(message.from_user.id, ClientState.phone, message.chat.id)
    await bot.send_message(message.chat.id, TextMsg.TYPE_PHONE)

    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['address'] = message.text


async def client_get_phone_handler(message: Message, bot: AsyncTeleBot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if not is_phone(message.text):
            await bot.send_message(message.chat.id, TextMsg.INCORRECT_PHONE)
            await bot.set_state(message.from_user.id, ClientState.phone, message.chat.id)

        else:
            data['phone'] = message.text
            await bot.send_message(message.chat.id, TextMsg.TYPE_ABOUT_CLIENT, reply_markup=add_client_about_is_none())
            await bot.set_state(message.from_user.id, ClientState.about_client, message.chat.id)


async def client_state_get_about_client_handler(message: Message, bot: AsyncTeleBot):
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if TextBtn.ABOUT_IS_NONE in message.text:
            data['about_client'] = None
        else:
            data['about_client'] = message.text

        await client_add_confirm_msg(message, bot, data)


async def client_add_confirm_msg(message: Message, bot: AsyncTeleBot, data):
    await bot.send_message(message.chat.id, TextMsg.CLIENT_ADD_CONFIRM(data), parse_mode='Markdown', reply_markup=add_client_confirm_keyboard())


async def client_add_callback_handler(callback: CallbackQuery, bot: AsyncTeleBot):
    chat_id = callback.message.chat.id
    message_id = callback.message.id

    api = API(bot, chat_id)

    if Handlers.CLIENT_CANCEL_ADD_STATE_TO_DB in callback.data:
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, TextMsg.CANCELED, reply_markup=clients_actions_keyboard())

    if Handlers.CLIENT_ADD_STATE_TO_DB in callback.data:
        async with bot.retrieve_data(chat_id) as data:
            response = await api.create_client(message_id, data)

            await bot.send_message(chat_id, f'{response["message"]}', reply_markup=clients_actions_keyboard())
            await bot.delete_message(chat_id, message_id)

        await bot.delete_state(chat_id)

    if Handlers.CLIENT_EDIT_STATE in callback.data:
        await bot.delete_message(chat_id, message_id)
        await bot.delete_state(chat_id)
        await client_state_start_handler(callback.message, bot)


def register_add_client_state_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(client_state_cancel_handler, regexp=TextMsg.CANCEL_ADD_CLIENT, state="*", pass_bot=True)
    bot.register_message_handler(client_state_start_handler, pass_bot=True, commands=['add_client_to_db'])

    bot.register_message_handler(client_get_first_name_handler, pass_bot=True, state=ClientState.first_name)
    bot.register_message_handler(client_get_last_name_handler, pass_bot=True, state=ClientState.last_name)
    bot.register_message_handler(client_get_patronymic_handler, pass_bot=True, state=ClientState.patronymic)
    bot.register_message_handler(client_get_city_handler, pass_bot=True, state=ClientState.city)
    bot.register_message_handler(client_get_address_handler, pass_bot=True, state=ClientState.address)
    bot.register_message_handler(client_get_phone_handler, pass_bot=True, state=ClientState.phone)
    bot.register_message_handler(client_state_get_about_client_handler, pass_bot=True, state=ClientState.about_client)

    bot.register_callback_query_handler(
        client_add_callback_handler,
        pass_bot=True, func=lambda callback: True if Handlers.ADD_CLIENT_PREFIX in callback.data else False
    )
