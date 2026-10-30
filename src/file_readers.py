import logging

import pandas as pd

from pathlib import Path

logger = logging.getLogger(__name__)

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_transactions_from_csv(file_path: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    logger.info(f"Чтение данных из CSV: {file_path}")

    try:
        # Читаем CSV
        df = pd.read_csv(file_path)
        # Превращаем таблицу в список словарей
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла: {e}")
        return []


def get_transactions_from_excel(file_path: str) -> list[dict]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""
    logger.info(f"Чтение данных из Excel: {file_path}")

    try:
        # Читаем Excel (для этого нужна библиотека openpyxl)
        df = pd.read_excel(file_path)
        # Превращаем таблицу в список словарей
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла: {e}")
        return []


if __name__ == "__main__":
    # Проверка работы (пути подставь свои)
    print(get_transactions_from_csv("data/transactions.csv")[:2])
    print(get_transactions_from_excel("data/transactions_excel.xlsx")[:2])