import json
from pathlib import Path
from typing import List
from statistics import mean

def analyze_logs(log_file: str):
    path = Path(log_file)
    if not path.exists():
        print(f"Файл '{log_file}' не найден.")
        return

    with path.open("r", encoding="utf-8") as f:
        logs = [json.loads(line) for line in f if line.strip()]

    if not logs:
        print("Лог пуст.")
        return

    total = len(logs)
    relevant_count = sum(1 for entry in logs if entry.get("relevant"))
    durations: List[float] = [entry["duration"] for entry in logs if "duration" in entry]

    print("=" * 40)
    print(f"Всего ответов: {total}")
    print(f"Подходящих ответов: {relevant_count} ({relevant_count / total * 100:.2f}%)")
    print(f"Неподходящих: {total - relevant_count} ({(total - relevant_count) / total * 100:.2f}%)")
    if durations:
        print(f"Среднее время генерации: {mean(durations):.3f} сек")
        print(f"Максимальное время генерации: {max(durations):.3f} сек")
        print(f"Минимальное время генерации: {min(durations):.3f} сек")
    else:
        print("Нет данных о времени.")
    print("=" * 40)

if __name__ == "__main__":
    analyze_logs("faq_log.jsonl")
