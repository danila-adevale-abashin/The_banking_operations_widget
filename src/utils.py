import json

import os

def get_operation_transactions(file_name: str) -> list[dict]:
    """Функция обрабатывает JSON-файл и выдаёт список словарей с данными о финансовых транзакциях"""
    if not os.path.exists(file_name):
        print("Файл не найден по данному пути!")
        return []

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Поймана ошибка: {type(e).__name__} - {e}")
        return []

    if not isinstance(data, list):
        print("Данные не являются списком!")
        return []

    return data


if __name__ == '__main__':
    print(get_operation_transactions('data/operations.json'))