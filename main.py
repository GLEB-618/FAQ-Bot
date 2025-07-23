from embedding_model import combine_faq_answers
from LLM_model import build_prompt, generate_response
import json
from utils import Timer

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

def log_response(question: str, answer: str, relevant: bool, duration: float) -> None:
    log_entry = {
        "question": question,
        "answer": answer,
        "relevant": relevant,
        "duration": round(duration, 4)
    }

    with open("faq_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

test_questions = [
    "Хочу сменить свой пароль, как это сделать?",
    "Как деактивировать учётку временно?",
    "Как подключить новый способ оплаты?",
    "Куда мне написать, если что-то не работает?",
    "Где найти свои прошлые заказы?",
    "Что я могу сделать с паролем?"
]

for question in test_questions:
    with Timer(label="Response generation") as t:
        print(f"Вопрос: {question}")
        qa_list, many_similar, avg, top_ans = combine_faq_answers(question, faq)
        if many_similar or avg:
            answer = generate_response(build_prompt(question, qa_list))
        else:
            answer = top_ans
        print(f"Ответ: {answer}\n\n")
    k = input("Подходит ли ответ? y/n ") == "y"
    log_response(question, answer, k, t.elapsed)
    
        
