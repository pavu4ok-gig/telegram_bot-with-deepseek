from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.deepseek_request import SendRequestToLLM

import logging

logging.basicConfig(level=logging.INFO)


router = Router()

req = SendRequestToLLM()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет пидоры')

@router.message(lambda message: message.text is not None)
async def handle_text(message: Message):
    print(f"ПОЛУЧЕНО: {message.text}")
    logging.info(f"Получено сообщение: {message.text} от {message.from_user.id}")
    output = req.get_answer(message.text)
    await message.answer(output)

#isPause = False

"""

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет пидоры')

@router.message()
async def answer_msg(message: Message):
    if message.from_user.id != 808326666 and isPause == False:
        await message.answer('ты пидор')

@router.message(F.text == 'нет ты пидор' or F.text == 'Нет ты пидор')
async def answer_msg2(message: Message):
   if message.from_user.id != 808326666 and isPause == False:
        await message.reply('нет, ты пидор')

@router.message(F.text == ('Иди нахуй').lower())
async def answer_back(message: Message):
    if message.from_user.id != 808326666 and isPause == False:
        await message.reply('нет, ты иди нахуй')

@router.message(Command('pause'))
async def set_pause(message: Message):
    global isPause
    if message.from_user.id == 808326666:
        isPause != isPause
        print(isPause)
    else:
        message.reply('Пашел нахуй нищий')

"""