from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_calendar import DialogCalendar, DialogCalendarCallback

from handlers.common import send_main_menu
from services.birthday_service import add_birthday, get_birthdays_for_chat, is_duplicate_name
from states.birthday_states import BirthdayForm

router = Router()


@router.callback_query(F.data == "get_bd")
async def log_birthdays(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BirthdayForm.waiting_for_name)
    await callback.message.answer("What's your name?")
    await callback.answer("Done!")


@router.message(BirthdayForm.waiting_for_name)
async def get_name(msg: Message, state: FSMContext) -> None:
    name = msg.text.strip()
    if not name:
        await msg.answer("Please enter a valid name.")
        return

    chat_id = msg.chat.id

    if await is_duplicate_name(chat_id, name):
        await msg.answer(
            f"{name} is already logged in this chat. Please enter a different name, or /cancel."
        )
        return

    await state.update_data(username=name, chat_id=chat_id)
    await state.set_state(BirthdayForm.waiting_for_birthday)
    await msg.answer(
        f"Nice to meet you, {name}!\nWhen's your birthday?",
        reply_markup=await DialogCalendar().start_calendar(),
    )


@router.callback_query(BirthdayForm.waiting_for_birthday, DialogCalendarCallback.filter())
async def get_bd(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext) -> None:
    selected, date = await DialogCalendar().process_selection(callback, callback_data)
    if not selected:
        return  # user is still picking year/month — calendar edits itself, nothing to save yet

    data = await state.get_data()
    name = data.get("username")
    chat_id = data.get("chat_id")

    await add_birthday(chat_id, name, date)
    await state.clear()
    await callback.message.answer(
        f"Name and Birthday Logged!\n\n{name}'s birthday is on {date.strftime('%d.%m.%Y')}."
    )
    await send_main_menu(callback.message)


@router.callback_query(F.data == "view_bd")
async def show_birthday_table(callback: CallbackQuery) -> None:
    birthdays = await get_birthdays_for_chat(callback.message.chat.id)
    if not birthdays:
        await callback.message.answer("No Birthdays Logged.")
    else:
        text = "Birthdays:\n\n"
        for user in birthdays:
            text += f"- {user.name}: {user.birthday}\n"
        await callback.message.answer(text)
    await callback.answer()
    await send_main_menu(callback.message)
