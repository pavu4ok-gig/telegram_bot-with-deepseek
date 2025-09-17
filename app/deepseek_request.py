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
            timeout=30
        )
        self.last_request_time = 0
        self.min_interval = 5  # 5 секунд между запросами
    
    def get_answer(self, promt):
        # Принудительная задержка между запросами
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            logger.info(f"⏳ Ожидание {sleep_time:.1f} сек перед запросом")
            time.sleep(sleep_time)
        
        logger.info('🔄 Отправлен запрос к DeepSeek')
        self.last_request_time = time.time()
        
        for attempt in range(3):
            try:
                completion = self.client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {
                            "role": "user", 
                            "content": f"Ответь кратко (максимум 100 слов): {promt}"
                        }
                    ],
                    max_tokens=100,  # Ограничиваем длину
                    temperature=0.7
                )
                
                logger.info('✅ Получен ответ от DeepSeek')
                return completion.choices[0].message.content
                
            except RateLimitError as e:
                wait_time = 10 * (2 ** attempt)  # 10, 20, 40 секунд
                logger.warning(f"⚠️ Rate limit (попытка {attempt + 1}/3). Ожидание {wait_time} сек...")
                if attempt < 2:
                    time.sleep(wait_time)
                
            except Exception as e:
                logger.error(f"❌ Ошибка API: {e}")
                if attempt == 2:
                    return "Извините, сервис временно недоступен."
                time.sleep(3)
        
        return "Слишком много запросов. Попробуйте через минуту."
