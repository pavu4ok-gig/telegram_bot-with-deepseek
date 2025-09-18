import os
import asyncio
import logging
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request
from app.handlers import register_handlers
from app.config import BOT_TOKEN

# Правильный webhook URL с endpoint /webhook
WEBHOOK_URL = "https://telegram-bot-with-deepseek.onrender.com/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

# Используем современный lifespan вместо устаревших on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"Webhook set to: {WEBHOOK_URL}")
    
    yield
    
    # Shutdown
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update_data = await request.json()
        print(f"Received update: {update_data.get('update_id', 'unknown')}")
        
        update = Update(**update_data)
        await dp.feed_update(bot, update)
        
        return {"status": "ok"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"message": "Bot is running with webhook"}

# Добавляем POST handler для корневого пути (если Telegram по какой-то причине отправляет туда)
@app.post("/")
async def root_post():
    return {"error": "POST requests should go to /webhook endpoint"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
