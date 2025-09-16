import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from app.handlers import router

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def handle_request(request: web.Request):
    data = await request.json()  # ⚠ обязательно скобки
    update = types.Update(**data)
    await dp.feed_update(update)  # v3 метод
    return web.Response(text="ok")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_request)

if __name__ == "__main__":
    from aiogram.webhook.aiohttp_server import setup_application
    setup_application(app, dp, path=WEBHOOK_PATH)  # ⚠ передаем dp
    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)
