import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "7927535008:AAFAKK1ERU_ETk3TmwY3JNYHNz6TK29pJqI"

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

class RecipeState(StatesGroup):
    adding = State()
    deleting = State()
    searching = State()
    selecting = State()

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить рецепт"), KeyboardButton(text="Случайный рецепт")],
        [KeyboardButton(text="Список рецептов"), KeyboardButton(text="Удалить рецепт")],
        [KeyboardButton(text="Поиск по ингредиенту")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Я бот для кулинарных рецептов. Выберите действие:", reply_markup=keyboard)

@dp.message(F.text.lower() == "добавить рецепт")
async def add_recipe(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(RecipeState.adding)
    await message.answer("Отправь рецепт в формате:\n\n**Название; Ингредиенты (через запятую); Описание**")

@dp.message(RecipeState.adding)
async def save_recipe(message: types.Message, state: FSMContext):
    parts = message.text.split(";")
    if len(parts) != 3:
        await message.answer("Ошибка! Формат: **Название; Ингредиенты; Описание**")
        return

    name, ingredients, description = map(str.strip, parts)

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO recipes (name, ingredients, description) VALUES (%s, %s, %s)",
            (name, ingredients, description)
        )
        conn.commit()
        await message.answer(f"✅ Рецепт '{name}' добавлен!", reply_markup=keyboard)
    except psycopg2.IntegrityError:
        conn.rollback()
        await message.answer("❌ Ошибка! Рецепт с таким названием уже существует.")
    finally:
        cur.close()
        conn.close()

    await state.clear()

@dp.message(F.text.lower() == "случайный рецепт")
async def random_recipe(message: types.Message, state: FSMContext):
    await state.clear()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, ingredients, description FROM recipes ORDER BY RANDOM() LIMIT 1")
    recipe = cur.fetchone()
    cur.close()
    conn.close()

    if recipe:
        await message.answer(f"📌 **{recipe[0]}**\n\n📝 {recipe[2]}\n\n🍽 Ингредиенты: {recipe[1]}")
    else:
        await message.answer("❌ В базе пока нет рецептов!")

@dp.message(F.text.lower() == "список рецептов")
async def list_recipes(message: types.Message, state: FSMContext):
    await state.clear()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM recipes")
    recipes = cur.fetchall()
    cur.close()
    conn.close()

    if recipes:
        recipe_list = "\n".join([f"📌 {r[0]}" for r in recipes])
        await message.answer(f"📖 **Список рецептов:**\n{recipe_list}\n\nВыберите рецепт для подробностей или напишите его название.", reply_markup=keyboard)
        await state.set_state(RecipeState.selecting)
    else:
        await message.answer("❌ В базе пока нет рецептов!")

@dp.message(RecipeState.selecting)
async def select_recipe(message: types.Message, state: FSMContext):
    recipe_name = message.text.strip()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, ingredients, description FROM recipes WHERE name = %s", (recipe_name,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()

    if recipe:
        await message.answer(f"📌 **{recipe[0]}**\n\n📝 {recipe[2]}\n\n🍽 Ингредиенты: {recipe[1]}")
    else:
        await message.answer(f"❌ Рецепта с названием '{recipe_name}' не найдено!")

    await state.clear()

@dp.message(F.text.lower() == "удалить рецепт")
async def delete_recipe(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(RecipeState.deleting)
    await message.answer("✏️ Отправь название рецепта, который хочешь удалить.")

@dp.message(RecipeState.deleting)
async def delete_recipe_by_name(message: types.Message, state: FSMContext):
    recipe_name = message.text.strip()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM recipes WHERE name = %s", (recipe_name,))
    recipe = cur.fetchone()

    if recipe:
        cur.execute("DELETE FROM recipes WHERE name = %s", (recipe_name,))
        conn.commit()
        await message.answer(f"🗑 Рецепт '{recipe_name}' удалён.")
    else:
        await message.answer(f"❌ Рецепта с названием '{recipe_name}' не существует.")

    cur.close()
    conn.close()
    await state.clear()

@dp.message(F.text.lower() == "поиск по ингредиенту")
async def search_recipe(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(RecipeState.searching)
    await message.answer("🔍 Введите ингредиент, по которому хотите найти рецепты.")

@dp.message(RecipeState.searching)
async def search_by_ingredient(message: types.Message, state: FSMContext):
    ingredient = message.text.strip().lower()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, ingredients, description FROM recipes WHERE LOWER(ingredients) LIKE %s", (f"%{ingredient}%",))
    recipes = cur.fetchall()
    cur.close()
    conn.close()

    if recipes:
        response = "\n\n".join([f"📌 **{r[0]}**\n📝 {r[2]}\n🍽 Ингредиенты: {r[1]}" for r in recipes])
        await message.answer(response)
    else:
        await message.answer(f"❌ Не найдено рецептов с ингредиентом '{ingredient}'.")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
