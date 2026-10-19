from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    :param transactions: Список словарей, содержащий информацию о транзакциях
    :param currency: Параметр, определяющий фильтрацию по валюте
    :return: Итератор транзакции по выбранной валюте
    """
    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    :param transactions: Список словарей, содержащий информацию о транзакциях
    :return: Итератор описания транзакции
    """
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX
    :param start: Начало генерации
    :param end: Конец генерации
    :return: Сгенерированные номера карт
    """
    for number in range(start, end + 1):
        s = f'{number:016d}'
        formatted = f'{s[:4]} {s[4:8]} {s[8:12]} {s[12:16]}'
        yield formatted


if __name__ == '__main__':
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
            "description": "Перевод организации",
            "from": "Счет 38577962768156718588",
            "to": "Счет 84561300280574060168",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {
                    "name": "руб.",
                    "code": "RUB",
                },
            },
            "description": "Перевод организации",
            "from": "Счет 93696711958316059307",
            "to": "Счет 15433413039820262433",
        },
        {
            "id": 214024827,
            "state": "EXECUTED",
            "date": "2018-12-20T16:43:26.929246",
            "operationAmount": {
                "amount": "70946.18",
                "currency": {
                    "name": "EUR",
                    "code": "EUR",
                },
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 32655442526060924852",
            "to": "Счет 37995340993185452102",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD",
                },
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]

    transaction_rub = filter_by_currency(transactions, 'RUB')

    for i in range(2):
        print(next(transaction_rub))

    descriptions = transaction_descriptions(transactions)
    for _ in range(7):
        print(next(descriptions))

    for card_number in card_number_generator(1, 5):
        print(card_number)