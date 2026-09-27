from datetime import date

from sqlalchemy import select, func

from db import async_session, User1


async def is_duplicate_name(chat_id: int, name: str) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(User1).where(
                func.lower(User1.name) == name.lower(),
                User1.chat_id == chat_id,
            )
        )
        return result.scalar_one_or_none() is not None


async def add_birthday(chat_id: int, name: str, birthday: date) -> None:
    async with async_session.begin() as session:
        session.add(User1(name=name, birthday=birthday, chat_id=chat_id))


async def get_birthdays_for_chat(chat_id: int) -> list[User1]:
    async with async_session() as session:
        result = await session.execute(
            select(User1).where(User1.chat_id == chat_id)
        )
        return result.scalars().all()