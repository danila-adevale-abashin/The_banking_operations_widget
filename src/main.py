import json

from src.file_readers import get_transactions_from_csv, get_transactions_from_excel
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import get_operation_transactions
from src.widget import mask_account_card


def main():
    # Приветствие пользователя
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями."
        "Выберите необходимый пункт меню:"
        "\n1. Получить информацию о транзакциях из JSON-файла"
        "\n2. Получить информацию о транзакциях из CSV-файла"
        "\n3. Получить информацию о транзакциях из XLSX-файла"
    )

    choice = input("\nВаш выбор: ")

    # 1. Загрузка данных в зависимости от выбора
    if choice == "1":
        print("\nДля обработки выбран JSON-файл.\n")
        transactions = get_operation_transactions("data/operations.json")
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        transactions = get_transactions_from_csv("data/transactions.csv")
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        transactions = get_transactions_from_excel("data/transactions_excel.xlsx")
    else:
        print("Неверный выбор. Попробуйте ещё раз.")
        return

    # 2. Фильтрация по статусу
    valid_states = ("EXECUTED", "CANCELED", "PENDING")

    while True:
        user_state = input(
            "Введите статус, по которому необходимо выполнить фильтрацию."
            f"\nДоступные для фильтровки статусы: {', '.join(valid_states)}\n"
        )
        user_state = user_state.upper()
        if user_state in valid_states:
            break
        print(f'Статус операции "{user_state}" недоступен.')

    transactions = filter_by_state(transactions, user_state)
    print(f'Операции отфильтрованы по статусу "{user_state}"')

    # 3. Фильтрация по дате
    answer_about_date = input("Отсортировать операции по дате? Да/Нет\n").capitalize()
    if answer_about_date == "Да":
        order = input("Отсортировать по возрастанию или по убыванию?\n").lower()
        reverse = order == "по убыванию"
        transactions = sort_by_date(transactions, reverse=reverse)

    # 4. Фильтрация по валюте
    answer_about_currency = input("Выводить только рублевые транзакции? Да/Нет\n").capitalize()
    if answer_about_currency == "Да":
        transactions = [
            t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # 5. Фильтрация по описанию
    answer_about_filter_word = input(
        "Отфильтровать список транзакций по определенному слову в описании? " "Да/Нет\n"
    ).capitalize()
    if answer_about_filter_word == "Да":
        search = input("Введите строку для поиска:\n")
        transactions = process_bank_search(transactions, search)

    # Вывод результата
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций..." f"\nВсего банковских операций в выборке: {len(transactions)}")

    for t in transactions:
        date = t["date"][:10]
        description = t["description"]
        amount = t.get("operationAmount", {}).get("amount", "0")
        currency = t.get("operationAmount", {}).get("currency", {}).get("name", "руб.")
        from_account = t.get("from", "")
        to_account = t.get("to", "")

        from_masked = mask_account_card(from_account) if from_account else ""
        to_masked = mask_account_card(to_account) if to_account else ""

        print("\n" f"\n{date} {description}")

        if from_masked and to_masked:
            print(f"{from_masked} -> {to_masked}")
        elif from_masked:
            print(from_masked)
        elif to_masked:
            print(to_masked)

        print(f"Сумма: {amount} {currency}")


if __name__ == "__main__":
    main()
