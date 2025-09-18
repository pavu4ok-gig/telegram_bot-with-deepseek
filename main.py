import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request
from app.handlers import register_handlers
from app.config import BOT_TOKEN

app = FastAPI()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
register_handlers(dp)

# Для Render - URL будет автоматически назначен
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://your-app-name.onrender.com/webhook")

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

@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)
        print(f"Webhook set to: {WEBHOOK_URL}")

@app.on_event("shutdown") 
async def on_shutdown():
    await bot.session.close()

@app.get("/")
async def root():
    return {"message": "Bot is running with webhook on Render"}

# Блок if __name__ == "__main__": НЕ НУЖЕН для Render!

