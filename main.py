import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiohttp import web
import os

from app.handlers import router
from app.config import BOT_TOKEN

WEBHOOK_HOST = "https://telegram-bot-with-deepseek.onrender.com"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_PORT = int(os.environ.get("PORT", 8000))
WEBAPP_HOST = "0.0.0.0"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    await bot.delete_webhook()

async def handle_request(request):
    update = await request.json()
    telegram_update = update
    await dp.feed_update(telegram_update)
    return web.Response(text="ok")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_request)

async def main():
    await on_startup()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()
    print(f"Webhook server running on {WEBAPP_HOST}:{WEBAPP_PORT}")
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is off")