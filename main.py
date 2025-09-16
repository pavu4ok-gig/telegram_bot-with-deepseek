import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import setup_application

# Включаем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app.handlers import router
    logger.info("Router успешно импортирован")
except ImportError as e:
    logger.error(f"Ошибка импорта router: {e}")
    raise

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://telegram-bot-with-deepseek.onrender.com{WEBHOOK_PATH}"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

logger.info("Router успешно подключен к dispatcher")

async def on_startup():
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    logger.info(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown():
    try:
        await bot.delete_webhook()
        logger.info("Webhook удален")
    except Exception as e:
        logger.error(f"Ошибка при удалении webhook: {e}")
    finally:
        await bot.session.close()

# Добавляем тестовый маршрут для проверки
async def health_check(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get('/', health_check)  # Для проверки что сервер работает

if __name__ == "__main__":
    logger.info("Настройка приложения...")
    setup_application(app, dp, bot=bot, path=WEBHOOK_PATH)
    
    app.on_startup.append(lambda app: on_startup())
    app.on_shutdown.append(lambda app: on_shutdown())
    
    port = int(os.getenv("PORT", 10000))
    logger.info(f"Запуск сервера на порту {port}")
    web.run_app(app, host="0.0.0.0", port=port)
