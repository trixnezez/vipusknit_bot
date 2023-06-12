import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6112419100:AAEus4MUbQN8VyjfJ1w4MoK1ouHGpWcJPSQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет")

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Добро пожаловать в нашего телеграм-бота! Мы рады приветствовать вас и готовы помочь вам найти вакансии без опыта работы, идеальные для выпускников университетов. Также мы предлагаем информацию о вакансиях без опыта работы по государственным программам, которые могут быть интересны для вас. Наш бот также поможет вам найти образовательные программы в разных странах мира. Просто задайте свои вопросы и мы с радостью предоставим вам нужную информацию. Удачного пользования нашим ботом!")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)