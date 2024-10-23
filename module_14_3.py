from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''

bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

# Общая клавиатура
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton('Рассчитать')
button_info = types.KeyboardButton('Информация')
button_buy = types.KeyboardButton('Купить')  # Новая кнопка "Купить"
keyboard.add(button_calculate, button_info, button_buy)

# Создание инлайн клавиатуры
inline_keyboard = InlineKeyboardMarkup()
button_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_keyboard.add(button_calories, button_formulas)

# Описание продуктов. Для удобства проверки дз поместил в один файл.
# Продукты можно редактировать, при этом меняется количество кнопок.
name_of_product = ('Слива', 'Вишня', 'Малина', 'Виктория', 'Виноград')
description_of_product = (
'Вкус кисло-сладкий, насыщенный.', 'Сладкая, нежная, ярко-красная.', 'Крупная, сладкая, с небольшой кислинкой.',
'Сладкая, с плотной мякотью.', 'Cладкий, с гармоничным вкусом.')
price_of_product = (519, 545, 595, 700, 650)

# Инлайн клавиатура с продуктами
products_keyboard = InlineKeyboardMarkup()
for i in range(0, len(name_of_product)):
    button = InlineKeyboardButton(f'{name_of_product[i]}', callback_data='product_buying')
    products_keyboard.add(button)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Обработка расчета
@dp.message_handler(commands=['start'])
async def start_command(message):
    await message.answer("Привет!", reply_markup=keyboard)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inline_keyboard)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    formula = "(10 × вес (кг) + 6.25 × рост (см) - 5 × возраст (лет) + 5)"
    await call.message.answer(formula)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите ваш возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите ваш рост (в сантиметрах):')
    await UserState.next()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите ваш вес (в килограммах):')
    await UserState.next()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    age = data['age']
    growth = data['growth']
    weight = data['weight']

    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Ваша норма калорий: {calories:.0f} ккал")
    await state.finish()


# Обработка покупки
@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(0, len(name_of_product)):
        text = f'Название: {name_of_product[i]}\nОписание: {description_of_product[i]}\n Цена за 1кг: {price_of_product[i]} руб.'
        with open(f'{name_of_product[i]}.jpg', 'rb') as img:
            await message.answer_photo(img)
        await message.answer(text)
    await message.answer("Выберите продукт для покупки:", reply_markup=products_keyboard)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
