from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.deepseek_request import SendRequestToLLM
import logging

router = Router()

reg = SendRequestToLLM()

# Создаем один экземпляр для всех запросов
llm = SendRequestToLLM()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('bot started')

@router.message(lambda message: message.text is not None)
async def handle_text(message: Message):
    output = req.get_answer(message.text)
    await message.answer(output)

def register_handlers(dp):
    dp.include_router(router)
