from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.menus import main_menu_keyboard

router = Router()


async def send_main_menu(message: Message, is_start: bool = False) -> None:
    text = (
        "Welcome to the Birthday Bot!\n\nShare with friends to have all the birthdays in one place!"
        if is_start
        else "What would you like to do next?"
    )
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.message(Command("start"))
async def start(message: Message) -> None:
    await send_main_menu(message, is_start=True)


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("No active operation to cancel.")
        return
    await state.clear()
    await message.answer("Operation cancelled.")
    await send_main_menu(message)