import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import setup_application
from app.handlers import router

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

app = web.Application()

if __name__ == "__main__":
    # Используем встроенный механизм aiogram
    setup_application(app, dp, bot=bot, path=WEBHOOK_PATH)
    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)
