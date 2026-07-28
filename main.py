#comment 

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import os
import asyncio
import sqlite3

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot= Bot(token=TOKEN)
dp= Dispatcher()
class BirthdayForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_birthday = State()
database= sqlite3.connect("/database/database.sqlite")
cursor= database.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Birthdays(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Birthday TEXT
)               
""")
database.commit()

async def main_menu(message: Message, is_start: bool=False):
    keyboard= InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text= "Log Birthday", callback_data= "get_bd")],
            [InlineKeyboardButton(text= "View Birthdays", callback_data= "view_bd")]
        ]
    )
    if is_start:
        text= "Welcome to the Birthday Bot!\n\nShare with friends to have all the birthdays in one place!"
    else:
        text= "What would you like to do next?"
    await message.answer(text, reply_markup= keyboard)

@dp.message(Command("start"))
async def start(message: Message):
    await main_menu(message, is_start=True)

@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    current_state= await state.get_state()
    if current_state is None:
        await message.answer("No active operation to cancel.")
        return
    await state.clear()
    await message.answer("Operation cancelled.")
    await main_menu(message)

@dp.callback_query(F.data=="get_bd")
async def log_birthdays(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BirthdayForm.waiting_for_name)
    await callback.message.answer("What's your name?")
    await callback.answer("Done!")

async def main():
    await dp.start_polling(bot)

@dp.message(BirthdayForm.waiting_for_name)
async def get_name(msg: Message, state: FSMContext):
    name = msg.text.strip()
    if not name:
        await msg.answer("Please enter a valid name.")
        return
    await state.update_data(username= name)
    await state.set_state(BirthdayForm.waiting_for_birthday)
    await msg.answer(
        f"Nice to meet you, {name}!\nWhen's your birthday?\n\nExample Format (DD.MM.YYYY)"
    )

@dp.message(BirthdayForm.waiting_for_birthday)
async def get_bd(bd: Message, state: FSMContext):
    birthday = bd.text.strip()
    if not birthday:
        await bd.answer("Please enter a valid date.")
        return
    data= await state.get_data()
    name= data.get("username")
    cursor.execute("""
    INSERT INTO Birthdays (Name, Birthday)
    VALUES (?, ?)
    """, (name, birthday))
    database.commit()
    await state.clear()
    await bd.answer(
        f"Name and Birthday Logged!\n\n{name}'s birthday is on {birthday}."
    )
    await main_menu(bd)

@dp.callback_query(F.data== "view_bd")
async def show_birthday_table(callback: CallbackQuery):
    cursor.execute("SELECT Name, Birthday FROM Birthdays")
    birthdays= cursor.fetchall()
    if not birthdays:
        await callback.message.answer(
            "No Birthdays Logged.")
    else:
        text= "Birthdays:\n\n"
        for Name, Birthday in birthdays:
            text += f"- {Name}: {Birthday}\n"
        await callback.message.answer(text)
    await callback.answer()
    await main_menu(callback.message)

if __name__== "__main__":
    asyncio.run(main())