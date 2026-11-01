import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_transactions_from_csv(file_path: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    logger.info(f"Чтение данных из CSV: {file_path}")

    try:
        # Читаем CSV
        df = pd.read_csv(file_path, sep=";")
        df = df.fillna("")

        transactions = []
        for _, row in df.iterrows():
            transactions.append({
                'id': row['id'],
                'state': row['state'],
                'date': row['date'],
                'operationAmount': {
                    'amount': str(row['amount']),
                    'currency': {
                        'name': row['currency_name'],
                        'code': row['currency_code'],
                    },
                },
                'from': row['from'],
                'to': row['to'],
                'description': row['description'],
            })
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла: {e}")
        return []


def get_transactions_from_excel(file_path: str) -> list[dict]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""
    logger.info(f"Чтение данных из Excel: {file_path}")

    try:
        # Читаем Excel
        df = pd.read_excel(file_path)
        df = df.fillna("")

        transactions = []
        for _, row in df.iterrows():
            transactions.append({
                'id': row['id'],
                'state': row['state'],
                'date': row['date'],
                'operationAmount': {
                    'amount': str(row['amount']),
                    'currency': {
                        'name': row['currency_name'],
                        'code': row['currency_code'],
                    },
                },
                'from': row['from'],
                'to': row['to'],
                'description': row['description'],
            })
        return transactions
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла: {e}")
        return []