import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# 1. Тесты для функции filter_by_currency:

@pytest.fixture
def transactions():
    """Набор транзакций с разными валютами для тестов."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
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
                "currency": {"name": "USD", "code": "USD"},
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
                "currency": {"name": "руб.", "code": "RUB"},
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
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Счет 38577962768156718588",
            "to": "Счет 84561300280574060168",
        },
        {
            "id": 214024827,
            "state": "EXECUTED",
            "date": "2018-12-20T16:43:26.929246",
            "operationAmount": {
                "amount": "70946.18",
                "currency": {"name": "EUR", "code": "EUR"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 32655442526060924852",
            "to": "Счет 37995340993185452102",
        },
    ]


@pytest.fixture
def empty_transactions():
    """Пустой список транзакций."""
    return []


# ТЕСТ № 1. Фильтрация по валюте:

@pytest.mark.parametrize(
    'currency, id',
    [
    ('USD', [939719570, 142264268]),
    ('RUB', [873106923, 594226727]),
    ('EUR', [214024827]),
    ],
)
def test_filter_by_currency_returns_matching(transactions, currency, id):
    """
    Функция тестирует возврат транзакций по указанной валюте
    :param transactions: Список транзакций
    :param currency: Выбранная для фильтрации валюта
    :param id: Идентификатор транзакции
    :return: Отфильтрованная транзакция
    """
    result = list(filter_by_currency(transactions, currency))

    assert [i['id'] for i in result] == id
    assert all(i['operationAmount']['currency']['code'] == currency for i in result)


@pytest.mark.parametrize("currency, expected_count", [
    ("USD", 2),
    ("RUB", 2),
    ("EUR", 1),
])
def test_filter_by_currency_count(transactions, currency, expected_count):
    """Количество найденных транзакций совпадает с ожидаемым."""
    result = list(filter_by_currency(transactions, currency))
    assert len(result) == expected_count


# ТЕСТ № 2. Фильтрация по отсутствующей валюте:

def test_filter_by_currency_no_matches(transactions):
    """Если валюты нет — пустой результат."""
    result = list(filter_by_currency(transactions, "JPY"))
    assert result == []

@pytest.mark.parametrize("currency", ["JPY", "GBP", "CNY", "RUB" + "X"])

def test_filter_by_currency_unknown_currency(transactions, currency):
    """Несуществующая валюта — пустой список, не ошибка."""
    result = list(filter_by_currency(transactions, currency))
    assert result == []


# ТЕСТ № 3. Тест с пустым списком:

def test_filter_by_currency_empty_list(empty_transactions):
    """Пустой список на входе → пустой итератор, без ошибок."""
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []

#######################################################################################################################

# 2. Тесты функции transaction_descriptions:

# ТЕСТ № 1. Корректный вывод описаний по транзакциям:

def test_transaction_descriptions_returns_all(transactions):
    """Возвращает описания всех транзакций в правильном порядке."""
    result = list(transaction_descriptions(transactions))

    assert len(result) == len(transactions)
    assert result == [
        'Перевод организации',
        'Перевод со счета на счет',
        'Перевод со счета на счет',
        'Перевод организации',
        'Перевод со счета на счет',
    ]


def test_transaction_descriptions_preserves_order(transactions):
    """Порядок описаний совпадает с порядком транзакций."""
    result = list(transaction_descriptions(transactions))
    expected = [t['description'] for t in transactions]

    assert result == expected


@pytest.mark.parametrize('index, expected', [
    (0, 'Перевод организации'),
    (1, 'Перевод со счета на счет'),
    (2, 'Перевод со счета на счет'),
    (3, 'Перевод организации'),
    (4, 'Перевод со счета на счет'),
])
def test_transaction_descriptions_specific(transactions, index, expected):
    """Каждое описание соответствует своей транзакции."""
    result = list(transaction_descriptions(transactions))
    assert result[index] == expected

# ТЕСТ №2. Разное количество транзакций:

@pytest.mark.parametrize('count', [1, 2, 3, 5, 10])
def test_transaction_descriptions_count(count):
    """Работает с любым количеством транзакций."""
    transactions = [
        {'description': f'Описание {i}'}
        for i in range(count)
    ]

    result = list(transaction_descriptions(transactions))

    assert len(result) == count
    assert result == [f'Описание {i}' for i in range(count)]


def test_transaction_descriptions_single():
    """Одна транзакция — одно описание."""
    transactions = [{'description': 'Единственное'}]

    result = list(transaction_descriptions(transactions))

    assert result == ['Единственное']


def test_transaction_descriptions_many():
    """Много транзакций — все описания на месте."""
    transactions = [{'description': f'Описание {i}'} for i in range(100)]

    result = list(transaction_descriptions(transactions))

    assert len(result) == 100
    assert result[-1] == 'Описание 99'

# ТЕСТ №3. Пустой список:'

def test_transaction_descriptions_empty_list(empty_transactions):
    """Пустой список — пустой итератор, без ошибок."""
    result = list(transaction_descriptions(empty_transactions))
    assert result == []


def test_transaction_descriptions_empty_is_iterator(empty_transactions):
    """Возвращает итератор даже для пустого списка."""
    gen = transaction_descriptions(empty_transactions)
    assert iter(gen) is gen
    assert list(gen) == []


#######################################################################################################################

# 3. Тесты функции card_number_generator:

# ТЕСТ № 1. Правильные номера в заданном диапазоне:

def test_card_number_generator_range_1_to_5():
    """Генератор выдаёт номера от 1 до 5 в правильном порядке."""
    result = list(card_number_generator(1, 5))

    assert result == [
        '0000 0000 0000 0001',
        '0000 0000 0000 0002',
        '0000 0000 0000 0003',
        '0000 0000 0000 0004',
        '0000 0000 0000 0005',
    ]


def test_card_number_generator_range_length():
    """Количество номеров в диапазоне совпадает с ожидаемым."""
    result = list(card_number_generator(1, 100))
    assert len(result) == 100


def test_card_number_generator_single():
    """Диапазон из одного числа — одна строка."""
    result = list(card_number_generator(1, 1))
    assert result == ['0000 0000 0000 0001']


def test_card_number_generator_order():
    """Номера идут по возрастанию."""
    result = list(card_number_generator(10, 15))
    assert result == [
        '0000 0000 0000 0010',
        '0000 0000 0000 0011',
        '0000 0000 0000 0012',
        '0000 0000 0000 0013',
        '0000 0000 0000 0014',
        '0000 0000 0000 0015',
    ]


@pytest.mark.parametrize('number, expected', [
    (1, '0000 0000 0000 0001'),
    (100, '0000 0000 0000 0100'),
    (9999, '0000 0000 0000 9999'),
    (10000, '0000 0000 0001 0000'),
    (1000000, '0000 0000 0100 0000'),
    (100000000, '0000 0001 0000 0000'),
])
def test_card_number_generator_specific(number, expected):
    """Конкретное число → конкретный формат."""
    assert next(card_number_generator(number, number)) == expected


# ТЕСТ № 2. Корректность форматирования:

def test_card_number_generator_format_length():
    """Длина строки — 19 символов (16 цифр + 3 пробела)."""
    result = next(card_number_generator(1, 1))

    assert len(result) == 19


def test_card_number_generator_format_spaces():
    """Ровно 3 пробела — между 4 группами."""
    result = next(card_number_generator(1, 1))

    assert result.count(' ') == 3


def test_card_number_generator_format_groups():
    """4 группы по 4 цифры."""
    result = next(card_number_generator(1, 1))
    parts = result.split(' ')

    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)


def test_card_number_generator_format_digits():
    """Каждая группа — только цифры."""
    result = next(card_number_generator(1234, 1234))
    parts = result.split(' ')

    assert all(part.isdigit() for part in parts)


def test_card_number_generator_format_leading_zeros():
    """Ведущие нули сохраняются."""
    result = next(card_number_generator(1, 1))

    assert result.startswith('0000 0000 0000')


def test_card_number_generator_format_all_numbers():
    """Все номера в диапазоне имеют правильный формат."""
    for card in card_number_generator(1, 20):
        parts = card.split(' ')
        assert len(parts) == 4
        assert all(len(part) == 4 and part.isdigit() for part in parts)


# ТЕСТ № 3. Крайние значения и завершение:

def test_card_number_generator_min_value():
    """Минимальное значение — 0000 0000 0000 0001."""
    result = next(card_number_generator(1, 1))
    assert result == '0000 0000 0000 0001'


def test_card_number_generator_max_value():
    """Максимальное значение — 9999 9999 9999 9999."""
    result = next(card_number_generator(9999999999999999, 9999999999999999))
    assert result == '9999 9999 9999 9999'


@pytest.mark.parametrize('number, expected', [
    (1, '0000 0000 0000 0001'),
    (9, '0000 0000 0000 0009'),
    (10, '0000 0000 0000 0010'),
    (99, '0000 0000 0000 0099'),
    (100, '0000 0000 0000 0100'),
    (9999999999999999, '9999 9999 9999 9999'),
])
def test_card_number_generator_boundaries(number, expected):
    """Крайние значения диапазона."""
    assert next(card_number_generator(number, number)) == expected


def test_card_number_generator_empty_range():
    """Если start > end — пустой итератор, без ошибок."""
    result = list(card_number_generator(5, 3))
    assert result == []


def test_card_number_generator_reversed():
    """Разные start и end — правильный диапазон."""
    result = list(card_number_generator(3, 6))
    assert result == [
        '0000 0000 0000 0003',
        '0000 0000 0000 0004',
        '0000 0000 0000 0005',
        '0000 0000 0000 0006',
    ]
