import asyncio
from app.bot import bot

if __name__ == "__main__":
    asyncio.run(bot.polling(non_stop=True))
