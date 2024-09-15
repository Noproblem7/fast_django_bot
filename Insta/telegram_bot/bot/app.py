import logging
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests

API_TOKEN = '7105541234:AAGD1MDLbBWxvdJdH9-e4nyCWCdvbkzIhV4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

FASTAPI_URL = 'http://127.0.0.1:8001/users/register/'


@dp.message_handler(commands=['users'])
async def send_welcome(message: types.Message):
    users = requests.get('http://127.0.0.1:8001/users/').json()["items"]
    for user in users:
        await message.reply(f"""
        Username: {user['username']}\n
        email:{user['email']}\n
        password:{user['password']}\n
        """)


@dp.message_handler(commands=['posts'])
async def send_welcome(message: types.Message):
    users = requests.get('http://127.0.0.1:8001/posts/').json()["items"]
    for user in users:
        await message.reply(f"""
        Caption: {user['caption']}\n
        image_path:{user['image_path']}\n
        """)


class RegisterForm(StatesGroup):
    name = State()
    email = State()
    password = State()


@dp.message_handler(commands='register', state='*')
async def start_register(message: types.Message):
    await message.answer("Xush kelibsiz! Iltimos, ismingizni kiriting:")
    await RegisterForm.name.set()


@dp.message_handler(state=RegisterForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Rahmat! Endi email manzilingizni kiriting:")
    await RegisterForm.next()


@dp.message_handler(state=RegisterForm.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Rahmat! Endi parolingizni kiriting:")
    await RegisterForm.next()


@dp.message_handler(state=RegisterForm.password)
async def process_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)

    user_data = await state.get_data()
    user_name = user_data['name']
    user_email = user_data['email']
    user_password = user_data['password']

    async with aiohttp.ClientSession() as session:
        payload = {
            'username': user_name,
            'email': user_email,
            'password': user_password
        }
        async with session.post(FASTAPI_URL, json=payload) as response:
            if response.status == 200:
                await message.answer(
                    f"Ro'yxatdan muvaffaqiyatli o'tdingiz!\nIsmingiz: {user_name}\nEmailingiz: {user_email}")
            else:
                await message.answer(f"Ro'yxatdan o'tishda xatolik yuz berdi. {response.status}")


@dp.message_handler(commands='cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Roʻyxatdan oʻtish bekor qilindi.', reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
