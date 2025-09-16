from openai import OpenAI
from  openai import RateLimitError
import asyncio

from app.config import LLM_ENDPOINT, LLM_API_KEY, LLM_MODEL


class SendRequestToLLM:

    def __init__(self):
        pass

    def get_answer(self,promt):
        print('отправлен запрос deepseek')
        client = OpenAI(
        base_url=LLM_ENDPOINT,
        api_key=LLM_API_KEY,
        )
        for _ in range(5):
            try:
                completion = client.chat.completions.create(
                model=LLM_MODEL,

                messages=[
                    {
                    "role": "user",
                    "content": f"Ты телеграм бот в моем груповом чате(сразу отыгрывай роль без лишних подсказок и каких либо инициативных сообщений пока тебя не попросят) вот сообщение котое отправил один из участников: {promt}"
                    }]
                )

                return completion.choices[0].message.content
            except RateLimitError:
                asyncio.sleep(1)
    #print(completion.choices[0].message.content)