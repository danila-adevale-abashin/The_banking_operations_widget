def filter_by_state(operations: list[dict], state: str = 'EXECUTED') -> list[dict]:
    """
    Функция принимает список словарей банковских операций, и фильтрует его,
    выводя список по указанному ключу state
    :param operations: Список банковских операций
    :param state: Значение ключа state
    :return: Отфильтрованный список по значению ключа state
    """
    return [item for item in operations if item['state'] == state]


if __name__ == '__main__':
    dictionary = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

print(filter_by_state(dictionary))

print(filter_by_state(dictionary, 'CANCELED'))