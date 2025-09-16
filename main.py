import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from app.handlers import router

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://telegram-bot-with-deepseek.onrender.com{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def webhook_handler(request: web.Request):
    try:
        print("🔄 Получен webhook запрос")  # Отладочная информация
        data = await request.json()
        print(f"📥 Данные от Telegram: {data}")  # Показать что приходит
        update = types.Update(**data)
        await dp.feed_update(bot, update)
        print("✅ Update обработан успешно")
        return web.Response(text="OK")
    except Exception as e:
        print(f"❌ Ошибка обработки webhook: {e}")
        return web.Response(status=500, text=f"Error: {e}")

async def health_check(request):
    return web.Response(text="🤖 Bot is running!")

async def on_startup():
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    print(f"🔗 Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown():
    try:
        await bot.delete_webhook()
        print("🗑️ Webhook удален")
    except Exception as e:
        print(f"⚠️ Ошибка при удалении webhook: {e}")
    finally:
        await bot.session.close()

# Создаем приложение и регистрируем маршруты вручную
app = web.Application()
app.router.add_post(WEBHOOK_PATH, webhook_handler)  # 👈 Ручная регистрация!
app.router.add_get("/", health_check)  # Для проверки статуса

if __name__ == "__main__":
    app.on_startup.append(lambda app: on_startup())
    app.on_shutdown.append(lambda app: on_shutdown())
    
    port = int(os.getenv("PORT", 10000))
    print(f"🚀 Запуск сервера на порту {port}")
    web.run_app(app, host="0.0.0.0", port=port)
