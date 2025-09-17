from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.request_queue import request_queue
import logging

logging.basicConfig(level=logging.INFO)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('🤖 Привет! Бот работает с очередью запросов')

@router.message()
async def handle_text(message: Message):
    print(f"ПОЛУЧЕНО: {message.text}")
    logging.info(f"Получено сообщение: {message.text} от {message.from_user.id}")
    
    # Добавляем в очередь вместо немедленной обработки
    async def send_response(response_text):
        await message.answer(response_text)
    
    await request_queue.add_request(
        user_id=message.from_user.id,
        message_text=message.text,
        response_callback=send_response
    )
    
    # Сразу уведомляем пользователя
    queue_size = len(request_queue.queue)
    if queue_size > 0:
        await message.answer(f"⏳ Ваш запрос в очереди (позиция: {queue_size})")
