def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция принимает список словарей банковских операций, и фильтрует его,
    выводя список по указанному ключу state
    :param operations: Список банковских операций
    :param state: Значение ключа state
    :return: Отфильтрованный список по значению ключа state
    """

    # result = []
    # for item in operations:
    #     if item['state'] == state:
    #         result.append(item)
    # return result

    return [item for item in operations if item["state"] == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """
    Функция принимает список словарей банковских операций, и фильтрует его,
    выводя список, отсортированным по дате
    :param operations: Список банковских операций
    :param reverse: Направление сортировки
    :return: Отсортированнный по дате список
    """

    return sorted(operations, key=lambda item: item["date"], reverse=reverse)


if __name__ == "__main__":

    # Список для проверки
    dictionary = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Проверка функции со значением по умолчанию и с указанным значением
    print(filter_by_state(dictionary))

    print(filter_by_state(dictionary, "CANCELED"))

    # Проверка функции с сортировкой по умолчанию и с указанным направлением
    print(sort_by_date(dictionary))

    print(sort_by_date(dictionary, False))
