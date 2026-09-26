import os
import asyncio
from dotenv import load_dotenv

from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column

load_dotenv()

class Base(DeclarativeBase):
    pass

class User1(Base):
    __tablename__ = "Birthdays"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    birthday = mapped_column(String, nullable=False)

# external url for testing locally, internal url for actual implementation
database_url = os.getenv("INTERNAL_DATABASE_URL") or os.getenv("EXTERNAL_DATABASE_URL")

if database_url is None:
    raise RuntimeError("No database URL found — set DATABASE_URL or EXTERNAL_DATABASE_URL in your environment.")

async_database_url = database_url.replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1
)

engine = create_async_engine(async_database_url, pool_pre_ping=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# engine, connect, execute
async def async_main():

    async with engine.connect() as conn:
        print ("Engine connected. Database connection successful ☑️")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print ("Table created.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())