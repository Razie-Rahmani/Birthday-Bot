from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Log Birthday", callback_data="get_bd")],
            [InlineKeyboardButton(text="View Birthdays", callback_data="view_bd")],
        ]
    )