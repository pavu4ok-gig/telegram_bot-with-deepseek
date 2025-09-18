from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.deepseek_request import SendRequestToLLM

router = Router()

req = SendRequestToLLM()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('bot started')

@router.message(lambda message: message.text is not None)
async def handle_text(message: Message):
    output = req.get_answer(message.text)
    await message.answer(output)

def register_handlers(dp):
    dp.include_router(router)