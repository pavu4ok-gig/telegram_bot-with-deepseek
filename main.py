import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import setup_application
from app.handlers import router

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://ваш-домен.onrender.com/webhook

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def on_startup():
    # Устанавливаем webhook при запуске
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    print(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()

app = web.Application()

if __name__ == "__main__":
    setup_application(app, dp, bot=bot, path=WEBHOOK_PATH)
    
    # Добавляем startup и shutdown хендлеры
    app.on_startup.append(lambda app: on_startup())
    app.on_shutdown.append(lambda app: on_shutdown())
    
    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)
