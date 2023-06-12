import sqlite3
from aiogram import Bot, types
from aiogram.types import KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import link
import asyncio
import openai
import requests
import json
from EdgeGPT import Chatbot, ConversationStyle

API_TOKEN = '6112419100:AAEus4MUbQN8VyjfJ1w4MoK1ouHGpWcJPSQ'  # Замените на свой API-токен

markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Состояния FSM
class VacanciesForm(StatesGroup):
    specialization = State()
    city = State()
class EducationForm(StatesGroup):
    country = State()
    program = State()
    gpa = State()
    specialization = State()
class first_work(StatesGroup):
	specialization = State()
	city = State()
class molodezh(StatesGroup):
	specialization = State()
	city = State()
	

# Обработчик команды /start
@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message, state= FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # buttons = ["Вакансии без опыта работы", "Образовательные программы", "Что такое молодежная практика?","Первое рабочее место"]
    keyboard.row("Вакансии без опыта работы")
    keyboard.row("Образовательные программы")
    keyboard.row("Что такое молодежная практика?")
    keyboard.row("Первое рабочее место")
    await message.answer(
        "Добро пожаловать в наш телеграм-бот! Мы рады приветствовать Вас и готовы помочь найти вакансии без опыта работы, "
        "что идеально для выпускников университетов. Мы предоставляем информацию о вакансиях без опыта работы по "
        "государственным программам, которые могут быть интересны и полезны для Вас. Наш бот также поможет Вам "
        "найти образовательные программы в разных странах мира.\n\n"
        "Задавайте свои вопросы и мы с радостью ответим Вам, предложив нужную информацию.\n\n"
        "Удачного пользования нашим ботом!\n\n*Для возврата в главное меню напишите /start*",
        reply_markup=keyboard, parse_mode="Markdown"
    )
    await state.finish()


@dp.message_handler(Text(equals="Что такое молодежная практика?"))
async def molodezhnaya_praktika_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_back = types.KeyboardButton("Назад")
    molodezh_vacancies = types.KeyboardButton("Вакансии по программе Молодежная практика")
    keyboard.add(molodezh_vacancies)
    keyboard.add(button_back)

    await message.answer(
        "Молодежная практика предназначена для выпускников организаций образования с целью получения первоначального опыта работы по полученной профессии (специальности). "\
        "На молодежную практику направляются зарегистрированные безработные в возрасте не старше 29 лет в течение 3-х лет после завершения обучения. "\
        "Продолжительность молодежной практики составляет не более 12 месяцев, размер заработной платы в месяц составляет не менее 30 месячных расчетных показателей (МРП). " \
        "Для получения направления необходимо обратиться в центр занятости населения по месту жительства. \n\n"\
        "Контакты центров занятости населения можно узнать <a href='https://www.enbek.kz/ru/zaniatost/czn-contacts'>здесь</a>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


# Обработчик кнопки "Назад"
@dp.message_handler(Text(equals="Назад"), state="*")
async def back_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await start_handler(message, state)

#обработчикк выбора вакансий Молодежная практика
@dp.message_handler(Text(equals="Вакансии по программе Молодежная практика"))
async def vacancies_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row("IT")
    keyboard.row("Финансы")
    keyboard.row("Журналистика")
    keyboard.row("Юриспруденция")
    keyboard.row("Медицина")
    keyboard.row("Строительство и архитектура")
    keyboard.row("Сервисное обслуживание/производство")
    keyboard.row("Менеджмент")
    keyboard.row("Наука")
    await message.answer("Выберите специализацию:", reply_markup=keyboard)
    await molodezh.next()

#обработчик города после специализации
@dp.message_handler(state=molodezh.specialization)
async def city_handler(message: types.Message, state: FSMContext):
    specialization = message.text
    await state.update_data(specialization=specialization)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # buttons = ["Алмата","Астана","Атырау","Актобе"]
    keyboard.row("Алмата")
    keyboard.row("Астана")
    keyboard.row("Атырау")
    keyboard.row("Актобе")
    keyboard.row("Актау")
    keyboard.row("Жезказган")
    keyboard.row("Караганда")
    keyboard.row("Кокшетау")
    keyboard.row("Костанай")
    keyboard.row("Кызылорда")
    keyboard.row("Павлодар")
    keyboard.row("Петропавловск")
    keyboard.row("Семей")
    keyboard.row("Талдыкорган")
    keyboard.row("Тараз")
    keyboard.row("Темиртау")
    keyboard.row("Уральск")
    keyboard.row("Усть-каменогорск")
    keyboard.row("Шымкент")
    keyboard.row("Экибастуз")


    await message.answer("Выберите город:", reply_markup=keyboard)
    await molodezh.city.set()

# Обработчик выбора города																
@dp.message_handler(state=molodezh.city)
async def show_vacancies_handler(message: types.Message, state: FSMContext):
    specialization = (await state.get_data()).get('specialization')
    city = message.text.lower()
    await state.update_data(city=city)
    # print(city)
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()
    mera = 'Молодежная практика'
    cursor.execute(f"SELECT * FROM {city}_vacancies WHERE Специальность = '{specialization}' AND Мера NOT LIKE '' AND Мера NOT LIKE 'Первое%'")     
    vacancies = cursor.fetchall()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()
    # print(vacancies)
    if vacancies:
        page_size = 1  # Количество вакансий на странице
        total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц
        # print('check')
        data = await state.get_data()
        data['page'] = 1  # Изначально показываем первую страницу
        await state.set_data(data)
        await show_vacancies_page(message, state, page_size, total_pages)
        # print('1')
    else:
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        await message.answer("Вакансий не найдено.", reply_markup=keyboard)

# Обработчик нажатия кнопки "Назад"
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back', state=molodezh)
async def back_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    specialization = data['specialization']
    city = data['city']
    # print(city)

    await molodezh.previous()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("IT")
    keyboard.row("Финансы")
    keyboard.row("Журналистика")
    keyboard.row("Юриспруденция")
    keyboard.row("Медицина")
    keyboard.row("Строительство и архитектура")
    keyboard.row("Сервисное обслуживание/производство")
    keyboard.row("Менеджмент")
    keyboard.row("Наука")

    await callback_query.message.answer("Выберите специализацию:", reply_markup=keyboard)

# Функция для отображения страницы с вакансиями
async def show_vacancies_page(message: types.Message, state: FSMContext, page_size: int, total_pages: int):
    print('1')
    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = data['city']
    # print(city)
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()
    print('check1')
    mera = 'Молодежная практика'
    cursor.execute(f"SELECT * FROM {city}_vacancies WHERE Специальность = '{specialization}' AND Мера NOT LIKE '' AND Мера NOT LIKE 'Первое%'")     
    vacancies = cursor.fetchall()
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_vacancies = vacancies[start_index:end_index]
    # print(current_page_vacancies)
    
    text = f"Страница {page}/{total_pages}\n\n"
    for row in current_page_vacancies:
        print("ccheck")
        position = row[0]
        # professional_role_id = row[1]
        salary = row[2]
        company = row[3]
        date = row[4]
        district = row[5]
        employment_type = row[6]
        employment_type2 = row[7]
        skills = row[8]
        link = row[9]
        employment_support_measure = row[10]
        specialty = row[11]
        formatted_vacancy = f"Должность: {position}\n" \
              f"Зарплата: {salary}\n" \
              f"Компания: {company}\n" \
              f"Дата обьявления: {date}\n" \
              f"Район: {district}\n" \
              f"График работы: {employment_type}\n" \
              f"Тип занятости: {employment_type2}\n" \
              f"Ключевые навыки: {skills}\n" \
              f"Ссылка: {link}\n" \
              f"Мера содействия занятости: {employment_support_measure}\n" \
              f"Специальность: {specialty}"
        text += formatted_vacancy + "\n\n<b>Для возврата в главное меню напишите /start</b>"

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    prev_button = types.InlineKeyboardButton("Предыдущая страница", callback_data=f"prev_page:{city}")
    next_button = types.InlineKeyboardButton("Следующая страница", callback_data=f"next_page:{city}")
    back_button = types.InlineKeyboardButton("Назад", callback_data="back")
    cursor.close()
    conn.close()

    keyboard.row(prev_button, next_button)
    keyboard.add(back_button)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Отправка нового сообщения с пагинацией
    new_message = await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    # Обновление данных состояния FSM
    data['message_id'] = new_message.message_id
    await state.set_data(data)


# Обработчик нажатия кнопки "Следующая страница"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('next_page'), state=molodezh)
async def next_page_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = data['city']
    # print(city)

    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    mera = 'Молодежная практика'
    cursor.execute(f"SELECT * FROM {city}_vacancies WHERE Специальность = '{specialization}' AND Мера NOT LIKE '' AND Мера NOT LIKE 'Первое%'")     
    vacancies = cursor.fetchall()

    cursor.close()
    conn.close()

    page_size = 1  # Количество вакансий на странице
    total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

    if page < total_pages:
        data['page'] = page + 1
        await state.set_data(data)
        await show_vacancies_page(callback_query.message, state, page_size, total_pages)
    else:
        await callback_query.message.answer("Вы достигли последней страницы.")

# Обработчик нажатия кнопки "Предыдущая страница"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('prev_page'), state=molodezh)
async def prev_page_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = (await state.get_data()).get('city')
    # print(city)

    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()
    mera = 'Молодежная практика'
    cursor.execute(f"SELECT * FROM {city}_vacancies WHERE Специальность = '{specialization}' AND Мера NOT LIKE '' AND Мера NOT LIKE 'Первое%'")     
    vacancies = cursor.fetchall()

    cursor.close()
    conn.close()

    page_size = 1  # Количество вакансий на странице
    total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

    if page > 1:
        data['page'] = page - 1
        await state.set_data(data)
        await show_vacancies_page(callback_query.message, state, page_size, total_pages)
    else:
        await callback_query.message.answer("Вы на первой странице.")

@dp.message_handler(Text(equals="Первое рабочее место"))
async def first_work_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_back = types.KeyboardButton("Назад")
    button_first_work_vacancies = types.KeyboardButton("Вакансии по программе Первое рабочее место")
    keyboard.add(button_first_work_vacancies)
    keyboard.add(button_back)

    await message.answer(
        "Первое рабочее место – это работа для молодежи не старше 29 лет для предоставления профессиональных знаний и навыков на первом рабочем месте.\n"\
"Продолжительность работы на первом рабочем месте составляет не более 18 месяцев, после завершения участнику предоставляется постоянное рабочее место на срок не менее 12 месяцев.\n"\
"Заработная плата составляет не менее 30 месячных расчетных показателей (МРП).\n"\
"Для получения направления необходимо обратиться в центр занятости населения по месту жительства.\n"\
"Контакты центров занятости населения можно узнать <a href='https://www.enbek.kz/ru/zaniatost/czn-contacts'>здесь</a>\n",

        reply_markup=keyboard,
        parse_mode="HTML"
    )

#обработчикк выбора вакансий первая работа
@dp.message_handler(Text(equals="Вакансии по программе Первое рабочее место"))
async def vacancies_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row("IT")
    keyboard.row("Финансы")
    keyboard.row("Журналистика")
    keyboard.row("Юриспруденция")
    keyboard.row("Медицина")
    keyboard.row("Строительство и архитектура")
    keyboard.row("Сервисное обслуживание/производство")
    keyboard.row("Менеджмент")
    keyboard.row("Наука")
    await message.answer("Выберите специализацию:", reply_markup=keyboard)
    await first_work.next()

#обработчик города после специализации
@dp.message_handler(state=first_work.specialization)
async def city_handler(message: types.Message, state: FSMContext):
    specialization = message.text
    await state.update_data(specialization=specialization)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row("Алмата")
    keyboard.row("Астана")
    keyboard.row("Атырау")
    keyboard.row("Актобе")
    keyboard.row("Актау")
    keyboard.row("Жезказган")
    keyboard.row("Караганда")
    keyboard.row("Кокшетау")
    keyboard.row("Костанай")
    keyboard.row("Кызылорда")
    keyboard.row("Павлодар")
    keyboard.row("Петропавловск")
    keyboard.row("Семей")
    keyboard.row("Талдыкорган")
    keyboard.row("Тараз")
    keyboard.row("Темиртау")
    keyboard.row("Уральск")
    keyboard.row("Усть-каменогорск")
    keyboard.row("Шымкент")
    keyboard.row("Экибастуз")
    await message.answer("Выберите город:", reply_markup=keyboard)
    await first_work.city.set()

# Обработчик выбора города																#Добавить where-условие
@dp.message_handler(state=first_work.city)
async def show_vacancies_handler(message: types.Message, state: FSMContext):
    specialization = (await state.get_data()).get('specialization')
    city = message.text.lower()
    await state.update_data(city=city)
    # print(city)
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    # Получение списка вакансий для указанного города и специализации
    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND "Мера содействия занятости" LIKE "Первое рабочее место"')
    vacancies = cursor.fetchall()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    if vacancies:
        page_size = 1  # Количество вакансий на странице
        total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

        data = await state.get_data()
        data['page'] = 1  # Изначально показываем первую страницу
        await state.set_data(data)

        await show_vacancies_page(message, state, page_size, total_pages)
    else:
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        await message.answer("Вакансий не найдено.", reply_markup=keyboard)

# Обработчик нажатия кнопки "Назад"
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back', state=first_work)
async def back_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    specialization = data['specialization']
    city = data['city']
    # print(city)

    await first_work.previous()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("IT")
    keyboard.row("Финансы")
    keyboard.row("Журналистика")
    keyboard.row("Юриспруденция")
    keyboard.row("Медицина")
    keyboard.row("Строительство и архитектура")
    keyboard.row("Сервисное обслуживание/производство")
    keyboard.row("Менеджмент")
    keyboard.row("Наука")

    await callback_query.message.answer("Выберите специализацию:", reply_markup=keyboard)

# Функция для отображения страницы с вакансиями
async def show_vacancies_page(message: types.Message, state: FSMContext, page_size: int, total_pages: int):
    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = data['city']
    # print(city)
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND "Мера содействия занятости" LIKE "Первое рабочее место"')
    vacancies = cursor.fetchall()

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_vacancies = vacancies[start_index:end_index]

    cursor.close()
    conn.close()

    text = f"Страница {page}/{total_pages}\n\n"
    for row in current_page_vacancies:
        position = row[0]
        professional_role_id = row[1]
        salary = row[2]
        company = row[3]
        date = row[4]
        district = row[5]
        employment_type = row[6]
        employment_type2 = row[7]
        skills = row[8]
        link = row[9]
        employment_support_measure = row[10]
        specialty = row[11]
        formatted_vacancy = f"Должность: {position}\n" \
              f"Зарплата: {salary}\n" \
              f"Компания: {company}\n" \
              f"Дата обьявления: {date}\n" \
              f"Район: {district}\n" \
              f"График работы: {employment_type}\n" \
              f"Тип занятости: {employment_type2}\n" \
              f"Ключевые навыки: {skills}\n" \
              f"Ссылка: {link}\n" \
              f"Мера содействия занятости: {employment_support_measure}\n" \
              f"Специальность: {specialty}"
        text += formatted_vacancy + "\n\n<b>Для возврата в главное меню напишите /start</b>"

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    prev_button = types.InlineKeyboardButton("Предыдущая страница", callback_data=f"prev_page:{city}")
    next_button = types.InlineKeyboardButton("Следующая страница", callback_data=f"next_page:{city}")
    back_button = types.InlineKeyboardButton("Назад", callback_data="back")

    keyboard.row(prev_button, next_button)
    keyboard.add(back_button)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Отправка нового сообщения с пагинацией
    new_message = await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    # Обновление данных состояния FSM
    data['message_id'] = new_message.message_id
    await state.set_data(data)


# Обработчик нажатия кнопки "Следующая страница"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('next_page'), state=first_work)
async def next_page_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = data['city']
    # print(city)

    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND "Мера содействия занятости" LIKE "Первое рабочее место"')
    vacancies = cursor.fetchall()

    cursor.close()
    conn.close()

    page_size = 1  # Количество вакансий на странице
    total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

    if page < total_pages:
        data['page'] = page + 1
        await state.set_data(data)
        await show_vacancies_page(callback_query.message, state, page_size, total_pages)
    else:
        await callback_query.message.answer("Вы достигли последней страницы.")

# Обработчик нажатия кнопки "Предыдущая страница"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('prev_page'), state=first_work)
async def prev_page_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = (await state.get_data()).get('city')
    # print(city)

    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND "Мера содействия занятости" LIKE "Первое рабочее место"')
    vacancies = cursor.fetchall()

    cursor.close()
    conn.close()

    page_size = 1  # Количество вакансий на странице
    total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

    if page > 1:
        data['page'] = page - 1
        await state.set_data(data)
        await show_vacancies_page(callback_query.message, state, page_size, total_pages)
    else:
        await callback_query.message.answer("Вы на первой странице.")

# Обработчик кнопки "Вакансии без опыта работы"
@dp.message_handler(Text(equals="Вакансии без опыта работы"))
async def vacancies_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.row("IT")
    keyboard.row("Финансы")
    keyboard.row("Журналистика")
    keyboard.row("Юриспруденция")
    keyboard.row("Медицина")
    keyboard.row("Строительство и архитектура")
    keyboard.row("Сервисное обслуживание/производство")
    keyboard.row("Менеджмент")
    keyboard.row("Наука")
    await message.answer("Выберите специализацию:", reply_markup=keyboard)
    await VacanciesForm.next()

@dp.message_handler(state=VacanciesForm.specialization)
async def city_handler(message: types.Message, state: FSMContext):
    specialization = message.text
    await state.update_data(specialization=specialization)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row("Алмата")
    keyboard.row("Астана")
    keyboard.row("Атырау")
    keyboard.row("Актобе")
    keyboard.row("Актау")
    keyboard.row("Жезказган")
    keyboard.row("Караганда")
    keyboard.row("Кокшетау")
    keyboard.row("Костанай")
    keyboard.row("Кызылорда")
    keyboard.row("Павлодар")
    keyboard.row("Петропавловск")
    keyboard.row("Семей")
    keyboard.row("Талдыкорган")
    keyboard.row("Тараз")
    keyboard.row("Темиртау")
    keyboard.row("Уральск")
    keyboard.row("Усть-каменогорск")
    keyboard.row("Шымкент")
    keyboard.row("Экибастуз")
    await message.answer("Выберите город:", reply_markup=keyboard)
    await VacanciesForm.city.set()

# Обработчик выбора города
@dp.message_handler(state=VacanciesForm.city)
async def show_vacancies_handler(message: types.Message, state: FSMContext):
    specialization = (await state.get_data()).get('specialization')
    city = message.text.lower()
    await state.update_data(city=city)
    # print(city)
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    # Получение списка вакансий для указанного города и специализации
    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND Мера LIKE ""')
    vacancies = cursor.fetchall()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    if vacancies:
        page_size = 1  # Количество вакансий на странице
        total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

        data = await state.get_data()
        data['page'] = 1  # Изначально показываем первую страницу
        await state.set_data(data)

        await show_vacancies_page(message, state, page_size, total_pages)
    else:
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data="back")
        keyboard.add(back_button)
        await message.answer("Вакансий не найдено.", reply_markup=keyboard)

# Обработчик нажатия кнопки "Назад"
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back', state=VacanciesForm)
async def back_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    specialization = data['specialization']
    city = data['city']
    # print(city)

    await VacanciesForm.previous()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("IT")
    keyboard.row("Финансы")
    keyboard.row("Журналистика")
    keyboard.row("Юриспруденция")
    keyboard.row("Медицина")
    keyboard.row("Строительство и архитектура")
    keyboard.row("Сервисное обслуживание/производство")
    keyboard.row("Менеджмент")
    keyboard.row("Наука")
    await callback_query.message.answer("Выберите специализацию:", reply_markup=keyboard)

# Функция для отображения страницы с вакансиями
async def show_vacancies_page(message: types.Message, state: FSMContext, page_size: int, total_pages: int):
    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = data['city']
    # print(city)
    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND Мера LIKE ""')

    vacancies = cursor.fetchall()
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_page_vacancies = vacancies[start_index:end_index]

    cursor.close()
    conn.close()

    text = f"Страница {page}/{total_pages}\n\n"
    for row in current_page_vacancies:
        position = row[0]
        professional_role_id = row[1]
        salary = row[2]
        company = row[3]
        date = row[4]
        district = row[5]
        employment_type = row[6]
        employment_type2 = row[7]
        skills = row[8]
        link = row[9]
        employment_support_measure = row[10]
        specialty = row[11]
        formatted_vacancy = f"Должность: {position}\n" \
              f"Зарплата: {salary}\n" \
              f"Компания: {company}\n" \
              f"Дата обьявления: {date}\n" \
              f"Район: {district}\n" \
              f"График работы: {employment_type}\n" \
              f"Тип занятости: {employment_type2}\n" \
              f"Ключевые навыки: {skills}\n" \
              f"Ссылка: {link}\n" \
              f"Мера содействия занятости: {employment_support_measure}\n" \
              f"Специальность: {specialty}"
        text += formatted_vacancy + "\n\n<b>Для возврата в главное меню напишите /start</b>"

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    prev_button = types.InlineKeyboardButton("Предыдущая страница", callback_data=f"prev_page:{city}")
    next_button = types.InlineKeyboardButton("Следующая страница", callback_data=f"next_page:{city}")
    back_button = types.InlineKeyboardButton("Назад", callback_data="back")

    keyboard.row(prev_button, next_button)
    keyboard.add(back_button)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Отправка нового сообщения с пагинацией
    new_message = await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    # Обновление данных состояния FSM
    data['message_id'] = new_message.message_id
    await state.set_data(data)


# Обработчик нажатия кнопки "Следующая страница"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('next_page'), state=VacanciesForm)
async def next_page_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = data['city']
    # print(city)

    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND Мера LIKE ""')
    vacancies = cursor.fetchall()

    cursor.close()
    conn.close()

    page_size = 1  # Количество вакансий на странице
    total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

    if page < total_pages:
        data['page'] = page + 1
        await state.set_data(data)
        await show_vacancies_page(callback_query.message, state, page_size, total_pages)
    else:
        await callback_query.message.answer("Вы достигли последней страницы.")

# Обработчик нажатия кнопки "Предыдущая страница"
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('prev_page'), state=VacanciesForm)
async def prev_page_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Отправляем пустой ответ, чтобы убрать уведомление о загрузке

    data = await state.get_data()
    page = data['page']
    specialization = data['specialization']
    city = (await state.get_data()).get('city')
    # print(city)

    conn = sqlite3.connect('vacancies.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {city}_vacancies WHERE Специальность LIKE "{specialization}" AND Мера LIKE ""')

    vacancies = cursor.fetchall()

    cursor.close()
    conn.close()

    page_size = 1  # Количество вакансий на странице
    total_pages = (len(vacancies) + page_size - 1) // page_size  # Общее количество страниц

    if page > 1:
        data['page'] = page - 1
        await state.set_data(data)
        await show_vacancies_page(callback_query.message, state, page_size, total_pages)
    else:
        await callback_query.message.answer("Вы на первой вакансии.")



# Обработчик кнопки "Образовательные программы"
@dp.message_handler(Text(equals="Образовательные программы"))
async def education_programs_handler(message: types.Message):    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Предпочитаемая страна образовательной программы:", reply_markup=keyboard )
    await EducationForm.country.set()

# Обработчик ввода страны
@dp.message_handler(state=EducationForm.country)
async def program_handler(message: types.Message, state: FSMContext):
    country = message.text
    await state.update_data(country=country)
    await message.answer("Предпочитаемая образовательная программа:", reply_markup=None)
    await EducationForm.program.set()

# Обработчик ввода программы
@dp.message_handler(state=EducationForm.program)
async def gpa_handler(message: types.Message, state: FSMContext):
    program = message.text
    await state.update_data(program=program)
    await message.answer("GPA студента:", reply_markup=None)
    await EducationForm.gpa.set()

# Обработчик ввода GPA
@dp.message_handler(state=EducationForm.gpa)
async def specialization_handler(message: types.Message, state: FSMContext):
    gpa = message.text
    await state.update_data(gpa=gpa)
    await message.answer("Специальность студента:", reply_markup=None)

    await EducationForm.specialization.set()


@dp.message_handler(state=EducationForm.specialization)
async def process_specialization(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['specialization'] = message.text
    await message.answer("Подождите 2-3 минуты, собирается информация")

    # Выполнение запроса к CHATGPT API для поиска образовательных программ
    response = await search_education_programs(data['country'], data['program'], data['gpa'], data['specialization'])
    # await message.answer("Подождите немного, собирается информация")
    await message.answer(response, parse_mode = "Markdown")
    await state.finish()

# Вспомогательная функция для выполнения запроса к CHATGPT API для поиска образовательных программ
async def search_education_programs(country, program, gpa, specialization):
    # Здесь выполняется запрос к CHATGPT API для поиска образовательных программ
    # cookies = json.loads(open("cookies.json", encoding="utf-8").read())
    # bot = (await Chatbot.create(cookies=cookies))
    # return (await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative))
    # await bot.close()
    cookies = json.loads(open("cookies.json", encoding="utf-8").read())
    bot = await Chatbot.create(cookies=cookies)
    response = await bot.ask(prompt=f"Подбери мне список образовательных программ {program} в стране {country} с моим GPA {gpa} и специальностью {specialization}. " \
                 "При этом твой ответ должен содержать меньше 4000 слов, " \
                 "поэтому опиши требования к образовательным программам максимально кратко, " \
                 "но выделив все самое важное и если есть, вставь ссылки на эти унвиерситеты, При этом выстави их в порядке убывания по рейтину университетов и в своем сообщении не упоминай, чт опоиск был произведен через Bing и не говори про требования к твоему ответу, иначе ", conversation_style=ConversationStyle.creative)
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]
    return str(bot_response + "\n\n*Для возврата в главное меню напишите /start*")
    # openai.api_key = "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"
    # api_key = "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"
    # headers = {
    #     "Authorization": f"Bearer {api_key}",
    #     "Content-Type": "application/json"
    # }
    # data = {
    #     "model": "gpt-4",
    #     "messages": [{"role": "user", "content": f"Подбери мне список образовательных программ {program} в стране {country} с моим GPA {gpa} и специальностью {specialization}. " \
    #              "При этом твой ответ должен содержать меньше 4000 слов, " \
    #              "поэтому опиши требования к образовательным программам максимально кратко, " \
    #              "но выделив все самое важное и вставь ссылки на сайты университетов, " \
    #              "при этом возьми всю информацию об актуальных образовательных программах из интернета " \
    #              "при помощи Python и обработай при помощи кода." \
    #              "Если магистратура юриспруденция, тогда не выводи Казахстанско-Британкий Технический университет"}],
    #     "temperature": 0.1
    # }

    # response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
    # result = response.json()
    # res = result['choices'][0]['message']['content']

    # Обработка и форматирование результатов поиска

    # return "Результаты поиска образовательных программ:\n\n" + str(res) + "\n\nДля возврата в главное меню напишите /start"


if __name__ == '__main__':
    asyncio.run(dp.start_polling())
