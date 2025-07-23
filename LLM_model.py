import requests
from config import URL_CHAT, LLM_MODEL

def build_prompt(user_question: str, qa_list: list[dict]) -> list[dict]:
    formatted_qa = ""
    for i, qa in enumerate(qa_list, 1):
        formatted_qa += f"{i}. Q: {qa['question']}\n   A: {qa['answer']}\n"

    system_message = (
        "Ты — FAQ-ассистент. Вот список вопросов и ответов, и вопрос пользователя.\n"
        "1. Если в вопросе затрагиваются несколько Q/A — объедини ответы.\n"
        "2. Если только один релевантен — выбери его и дай ответ.\n"
        "3. Если вопрос непонятен — попроси уточнить.\n"
        "Не придумывай ничего сам, опирайся только на предложенные Q/A.\n"
    )

    user_message = (
        f"Вопрос пользователя: {user_question}\n\n"
        f"Вот список Q/A из базы знаний:\n{formatted_qa}\n"
        "Сформулируй точный ответ пользователю, опираясь на них."
    )

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

def generate_response(messages: list[dict]) -> str:
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "num_predict": 2048
        }
    }

    response = requests.post(URL_CHAT, json=payload)
    response.raise_for_status()
    return response.json()["message"]["content"]