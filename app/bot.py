from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_handler_backends import BaseMiddleware, CancelUpdate

from actions.start.handlers import start_handler
from actions.clients.handlers.get_client import register_get_client_handlers, show_client_handler
from actions.clients.handlers.add_client import register_add_client_state_handlers
from common.utils import Bregexp
from common.enviroments import USERS_ID, TG_BOT_API_KEY

bot = AsyncTeleBot(TG_BOT_API_KEY)


class RoleMiddleware(BaseMiddleware):
    def __init__(self, users: list[int]) -> None:
        super().__init__()

        self.users = users
        self.update_types = ['message']
        # Always specify update types, otherwise middlewares won't work

    async def pre_process(self, message, data):
        if message.from_user.id in self.users:
            return
        else:
            await bot.send_message(message.chat.id, 'Кто ты')
            return CancelUpdate()

    async def post_process(self, message, data, exception):
        pass


# register handlers
bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)

register_get_client_handlers(bot)
register_add_client_state_handlers(bot)

bot.register_message_handler(
    show_client_handler,
    regexp=Bregexp.PHONE,
    pass_bot=True
)

# filters
bot.add_custom_filter(asyncio_filters.StateFilter(bot))

# middleware
bot.setup_middleware(RoleMiddleware(USERS_ID))
