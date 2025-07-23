from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config import FAQ_TOP_K, EMBEDDING_MODEL, THRESHOLD_DIFF

def combine_faq_answers(question: str, faq: list[dict]):

    faq_questions = [item["question"] for item in faq]
    faq_answers = [item["answer"] for item in faq]

    # Инициализация модели
    model = SentenceTransformer(EMBEDDING_MODEL)  # Загружается 1 раз

    # Векторизация FAQ
    faq_embeddings = model.encode(faq_questions)

    user_embedding = model.encode([question])
    sims = cosine_similarity(user_embedding, faq_embeddings)[0]

    top_indices = sims.argsort()[::-1][:FAQ_TOP_K] # Индексы самых близких вопросов. В порядке убывания
    top_values = [sims[i] for i in top_indices]

    max_sim = top_values[0]
    close_scores = len([s for s in top_values if abs(max_sim - s) < THRESHOLD_DIFF])
    avg_topk = sum(top_values) / FAQ_TOP_K

    print(f"Лучший ответ: {max_sim}")
    print(f"Одинаковые (по смыслу) запросы: {close_scores}")
    print(close_scores >= (FAQ_TOP_K - 1))
    print(f"Среднее значение: {avg_topk:.4f}")
    print(f"Разница между самым подходящим и средним: {(max_sim - avg_topk):.4f}")
    print((max_sim - avg_topk) < THRESHOLD_DIFF)

    qa_list = [
        {"question": faq_questions[idx], "answer": faq_answers[idx]} for idx in top_indices
    ]
    return qa_list, close_scores >= (FAQ_TOP_K - 1), (max_sim - avg_topk) < THRESHOLD_DIFF, faq_answers[top_indices[0]]