from typing import Tuple, Any, Dict
from functools import lru_cache

import config

from langchain_mistralai import ChatMistralAI
from langchain_community.chat_models import ChatYandexGPT
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from palimpsest import Palimpsest

import logging
logger = logging.getLogger(__name__)

# Setting up LLM
#llm = ChatMistralAI(model="mistral-small-latest", temperature=1, frequency_penalty=0.3)
"""
model_name=f'gpt://{config.YA_FOLDER_ID}/yandexgpt-32k/rc'
llm = ChatYandexGPT(
    #iam_token = None,
    api_key = config.YA_API_KEY, 
    folder_id=config.YA_FOLDER_ID, 
    model_uri=model_name,
    temperature=0.4
    )
"""
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.4, frequency_penalty=0.3)

processor = Palimpsest(verbose=True)

def anonymize(text: str, language = "en") -> str:
    resulting_text = processor.anonimize(text)
    return resulting_text

def deanonymize(text: str, language = "en") -> str:
    resulting_text = processor.deanonimize(text)
    return resulting_text


def generate_answer(system_prompt: str, user_request: str, llm_provider: str = "OpenAI", llm_parameters: Dict[str, Any] = {}) -> Tuple[str, str]:
    """
    Dummy LLM call. Replace with real API integration.
    Returns (llm_response, deanonymized_response).
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "{user_request}"),
        ]
    )
    processor.reset_context()
    anonymized_request = anonymize(user_request, language="en")

    chain = prompt | llm
    #chain = {"user_request": lambda txt: anonymize(txt, language="en")} | prompt | llm | (lambda ai_message: deanonymize(ai_message.content))
    response = chain.invoke(anonymized_request)
    llm_answer = response.content
    deanonymized_answer = deanonymize(llm_answer)
    return deanonymized_answer, anonymized_request, llm_answer

def get_llm_parameters(provider: str) -> Dict[str, str]:
    """
    Return default parameter names → values for each supported LLM provider.
    Update this dict when provider parameter sets change.
    """
    defaults = {
        "OpenAI": {
            "api_key": "",
            "model_spec": "gpt-4",
            "temperature": "0.7",
            "max_tokens": "1024"
        },
        "Mistral": {
            "api_key": "",
            "model_spec": "mist-1",
            "temperature": "0.7"
        },
        "Yandex": {
            "api_key": "",
            "model_spec": "yam-1",
            "temperature": "0.7",
            "folder_id": ""
        },
        "SberGIGA": {
            "api_key": "",
            "model_spec": "sbg-1",
            "temperature": "0.7"
        },
    }
    return defaults.get(provider, {}) if provider else defaults

if __name__ == "__main__":
    from palimpsest.logger_factory import setup_logging


    setup_logging("anonimizer_web_test", other_console_level=logging.DEBUG, project_console_level=logging.DEBUG)

    text = """Клиент Степан Степанов (4519227557) по поручению Ивана Иванова обратился в "Интерлизинг" с предложением купить трактор. 
    Для оплаты используется его карта 4095260993934932. 
    Позвоните ему 9867777777 или 9857777237.
    Или можно по адресу г. Санкт-Петербург, Сенная Площадь, д1/2кв17
    Посмотреть его данные можно https://client.ileasing.ru/name=stapanov:3000 или зайти на 182.34.35.12/
    """    
    system_prompt = """Преобразуй текст в записку для записи в CRM. Текст должен быть хорошо структурирован и понятен с первого взгляда"""
    print(generate_answer(system_prompt, text))
