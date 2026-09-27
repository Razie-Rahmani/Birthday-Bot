import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, HTTPException, Request

import logger_config as _
from config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_SECRET, WEBHOOK_URL
from db import Base, engine
from handlers import common, birthday_handlers

logger = logging.getLogger(__name__)
logger.info("🍃 Application Started 🍃")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(common.router)
dp.include_router(birthday_handlers.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    logger.info("🔥 WEBHOOK_URL = %s", WEBHOOK_URL)
    logger.info("🔥 WEBHOOK_SECRET configured = %s", bool(WEBHOOK_SECRET))
    result = await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    logger.info("🔥 set_webhook result = %s", result)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # --- shutdown ---
    await engine.dispose()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=403)
    data = await request.json()
    update = Update.model_validate(data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"ok": True}