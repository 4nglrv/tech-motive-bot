from telebot import TeleBot
from telebot.types import Message

from app.actions.start.keyboards import start_keyboard
from app.constants.text import TextBtn


async def start_handler(message: Message, bot: TeleBot):
    await bot.send_message(message.chat.id, TextBtn.CHOOSE_SECTION, reply_markup=start_keyboard())
