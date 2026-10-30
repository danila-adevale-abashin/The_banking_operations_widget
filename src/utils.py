import json
import logging
import os
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w", encoding="utf-8")

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_operation_transactions(file_name: str) -> list[dict]:
    """Функция обрабатывает JSON-файл и выдаёт список словарей с данными о финансовых транзакциях"""
    logger.info("Принят JSON-файл для прочтения")

    if not os.path.exists(file_name):
        logger.error("Файл не найден по данному пути!")
        print("Файл не найден по данному пути!")
        return []

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Поймана ошибка: {type(e).__name__} - {e}")
        print(f"Поймана ошибка: {type(e).__name__} - {e}")
        return []

    if not isinstance(data, list):
        logger.error("Данные не являются списком!")
        print("Данные не являются списком!")
        return []

    return data


if __name__ == "__main__":
    print(get_operation_transactions("data/operations.json"))
