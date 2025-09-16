from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import logging

logging.basicConfig(level=logging.INFO)
router = Router()

# Временно закомментируем проблемный импорт
try:
    from app.deepseek_request import SendRequestToLLM
    req = SendRequestToLLM()
    print("✅ SendRequestToLLM успешно инициализирован")
except Exception as e:
    print(f"❌ Ошибка инициализации SendRequestToLLM: {e}")
    req = None

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет! Бот запущен и работает!')

@router.message(lambda message: message.text is not None)
async def handle_text(message: Message):
    print(f"ПОЛУЧЕНО: {message.text}")
    logging.info(f"Получено сообщение: {message.text} от {message.from_user.id}")
    
    if req is None:
        await message.answer("⚠️ AI-модуль не загружен, но бот работает!")
        return
    
    try:
        output = req.get_answer(message.text)
        await message.answer(output)
    except Exception as e:
        print(f"Ошибка при обращении к AI: {e}")
        await message.answer(f"Ошибка AI: {str(e)}")


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