# coming up:
# ☑️ change polling to webhook 
# ☑️ register the webhook with telegram --> set_webhook()
# ☑️ Render start command: runs a ASGI server
# ☑️ environment variables
# ☑️ change sqlite to postgres render
# ☑️ deploy on render
# polish: make it look pretty, up UI
# upgrade: make it more modular (handlers/, services/, keyboards/, etc.)
# feat: delete/edit a bd if id is the same as the one entered (needs telegram checking ids)
# feat: sort dates generally
# feat: sort by upcoming date
# feat: admin panel (one main, one for each group) --> first feat: CRUD ops
# feat: create/join group (+ all its features)
# feat: add new events planner for each birthday (including place, people, theme, a way for the bd person to send an invitation to her firends, etc.)


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Update
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from fastapi import FastAPI, Request, Response, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import logging
import logger_config as _
from db import engine, async_session, Base, User1
from sqlalchemy import select, func

load_dotenv()

logger = logging.getLogger(__name__)
logger.info("🍃 Application Started 🍃")

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Lifespan Setup

@asynccontextmanager
async def lifespan(app: FastAPI):

    # --- startup ---
    logger.info("🔥 WEBHOOK_URL = %s", WEBHOOK_URL)
    logger.info("🔥 WEBHOOK_SECRET configured = %s", bool(WEBHOOK_SECRET))
    result = await bot.set_webhook(
        url = WEBHOOK_URL,
        secret_token = WEBHOOK_SECRET
    )
    logger.info("🔥 set_webhook result = %s", result) 

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # --- shutdown ---
    await engine.dispose()
    await bot.session.close()

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI(lifespan=lifespan)

class BirthdayForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_birthday = State()

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

@dp.message(BirthdayForm.waiting_for_name)
async def get_name(msg: Message, state: FSMContext):
    name = msg.text.strip()
    if not name:
        await msg.answer("Please enter a valid name.")
        return
    
    chat_id = msg.chat.id

    async with async_session() as session:
        result = await session.execute(
            select(User1).where(
                func.lower(User1.name) == name.lower(),
                User1.chat_id == chat_id
            )
        )
        existing = result.scalar_one_or_none()

    if existing:
        await msg.answer(
            f"{name} is already logged in this chat. Please enter a different name, or /cancel."
        )
        return

    await state.update_data(username=name, chat_id=chat_id)
    await state.set_state(BirthdayForm.waiting_for_birthday)
    await msg.answer(
        f"Nice to meet you, {name}!\nWhen's your birthday?",
        reply_markup=await DialogCalendar().start_calendar()
    )

@dp.callback_query(BirthdayForm.waiting_for_birthday, DialogCalendarCallback.filter())
async def get_bd(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    selected, date = await DialogCalendar().process_selection(callback, callback_data)
    if not selected:
        return  # user is still picking year/month — calendar edits itself, nothing to save yet

    data = await state.get_data()
    name = data.get("username")
    chat_id = data.get("chat_id")
    async with async_session.begin() as session:
        session.add(User1(name=name, birthday=date, chat_id=chat_id))
    await state.clear()
    await callback.message.answer(
        f"Name and Birthday Logged!\n\n{name}'s birthday is on {date.strftime('%d.%m.%Y')}."
    )
    await main_menu(callback.message)

@dp.callback_query(F.data== "view_bd")
async def show_birthday_table(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(User1).where(User1.chat_id == callback.message.chat.id)
        )
        birthdays = result.scalars().all()
    if not birthdays:
        await callback.message.answer(
            "No Birthdays Logged.")
    else:
        text= "Birthdays:\n\n"
        for user in birthdays:
            text += f"- {user.name}: {user.birthday}\n"
        await callback.message.answer(text)
    await callback.answer()
    await main_menu(callback.message)

# Webhook Configuration

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=403)
    data = await request.json()
    update = Update.model_validate(data, context={"bot" : bot})
    await dp.feed_update(bot, update)
    return {"ok" : True}