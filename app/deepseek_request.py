from openai import OpenAI
from openai import RateLimitError
import time
import logging
from app.config import LLM_ENDPOINT, LLM_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

class SendRequestToLLM:
    
    def __init__(self):
        self.client = OpenAI(
            base_url=LLM_ENDPOINT,
            api_key=LLM_API_KEY,
        )
    
    def get_answer(self, promt):
        logger.info('🔄 Отправлен запрос к DeepSeek')
        
        for attempt in range(5):
            try:
                completion = self.client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Ты телеграм бот в моем групповом чате (сразу отыгрывай роль без лишних подсказок и каких либо инициативных сообщений пока тебя не попросят) вот сообщение которое отправил один из участников: {promt}"
                        }
                    ]
                )
                
                logger.info('✅ Получен ответ от DeepSeek')
                return completion.choices[0].message.content
                
            except RateLimitError as e:
                wait_time = 2 ** attempt  # Экспоненциальная задержка: 1, 2, 4, 8, 16 сек
                logger.warning(f"⚠️ Rate limit exceeded (попытка {attempt + 1}/5). Ожидание {wait_time} сек...")
                time.sleep(wait_time)  # Используем time.sleep вместо asyncio.sleep
                
            except Exception as e:
                logger.error(f"❌ Ошибка при запросе к DeepSeek (попытка {attempt + 1}/5): {e}")
                if attempt == 4:  # Последняя попытка
                    return f"Извините, не могу ответить прямо сейчас. Ошибка: {str(e)}"
                time.sleep(1)
        
        # Если все попытки неудачны
        logger.error("❌ Все попытки обращения к DeepSeek неудачны")
        return "Извините, сервис временно недоступен. Попробуйте позже."
