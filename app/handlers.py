from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.deepseek_request import SendRequestToLLM
import logging

logging.basicConfig(level=logging.INFO)
router = Router()

# Создаем один экземпляр для всех запросов
llm = SendRequestToLLM()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('🤖 Привет! Бот работает с ограничениями API')

@router.message()
async def handle_text(message: Message):
    user_id = message.from_user.id
    print(f"ПОЛУЧЕНО: {message.text}")
    logging.info(f"Получено сообщение: {message.text} от {user_id}")
    
    try:
        # Простой вызов с автоматическими задержками
        output = llm.get_answer(message.text)
        await message.answer(output)
        
    except Exception as e:
        logging.error(f"Ошибка обработки сообщения: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")
