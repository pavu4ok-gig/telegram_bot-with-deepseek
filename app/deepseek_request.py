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
            timeout=30  # Ограничиваем время ожидания
        )
        self.last_request_time = 0
        self.min_interval = 2  # Минимум 2 секунды между запросами
    
    def get_answer(self, promt):
        # Ограничиваем частоту запросов
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            logger.info(f"⏳ Ожидание {sleep_time:.1f} сек перед запросом")
            time.sleep(sleep_time)
        
        logger.info('🔄 Отправлен запрос к DeepSeek')
        self.last_request_time = time.time()
        
        for attempt in range(3):  # Уменьшили до 3 попыток
            try:
                completion = self.client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Ты телеграм бот. Ответь кратко на: {promt}"
                        }
                    ],
                    max_tokens=150,  # Ограничиваем длину ответа
                    temperature=0.7
                )
                
                logger.info('✅ Получен ответ от DeepSeek')
                return completion.choices[0].message.content
                
            except RateLimitError as e:
                wait_time = min(10 * (2 ** attempt), 60)  # Максимум 60 сек
                logger.warning(f"⚠️ Rate limit (попытка {attempt + 1}/3). Ожидание {wait_time} сек...")
                if attempt < 2:  # Не ждем на последней попытке
                    time.sleep(wait_time)
                
            except Exception as e:
                logger.error(f"❌ Ошибка API (попытка {attempt + 1}/3): {e}")
                if attempt == 2:
                    return f"Извините, сервис временно недоступен."
                time.sleep(2)
        
        return "Извините, слишком много запросов. Попробуйте через минуту."
