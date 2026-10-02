import pytest

from src.processing import filter_by_state, sort_by_date

# 1. Тесты функции filter_by_state:


@pytest.mark.parametrize(
    "operations, state, expected",
    [
        # EXECUTED по умолчанию
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}],
        ),
        # CANCELED
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 256, "state": "CANCELED"}],
            "CANCELED",
            [{"id": 256, "state": "CANCELED"}],
        ),
        # PENDING
        (
            [{"id": 1, "state": "PENDING"}, {"id": 2, "state": "EXECUTED"}],
            "PENDING",
            [{"id": 1, "state": "PENDING"}],
        ),
    ],
)
def test_filter_by_state(operations, state, expected):
    assert filter_by_state(operations, state) == expected


def test_default_state():
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    assert filter_by_state(operations) == [{"id": 1, "state": "EXECUTED"}]


def test_no_match():
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    assert filter_by_state(operations, "PENDING") == []


@pytest.mark.parametrize(
    "state",
    [
        "PENDING",
        "FAILED",
        "UNKNOWN",
        "",
    ],
)
def test_no_matches(state):
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    assert filter_by_state(operations, state) == []


def test_empty_operations():
    assert filter_by_state([]) == []


def test_all_match():
    operations = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED"},
    ]
    assert filter_by_state(operations) == operations


# 2. Тесты функции sort_by_date:


@pytest.fixture
def client_operations():
    """Базовый набор операций для тестов."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def same_dates_operations():
    """Операции с одинаковыми датами — для проверки stable sort."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T10:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2024-03-11T10:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-03-11T10:00:00.000000"},
    ]


def test_sort_descending_default(client_operations):
    """По умолчанию — убывание: новые даты первыми."""
    result = sort_by_date(client_operations)

    assert [op["id"] for op in result] == [
        41428829,  # 2019-07-03
        615064591,  # 2018-10-14
        594226727,  # 2018-09-12
        939719570,  # 2018-06-30
    ]


def test_sort_descending_explicit(client_operations):
    """Явно reverse=True — то же, что по умолчанию."""
    result = sort_by_date(client_operations, reverse=True)

    assert [op["id"] for op in result] == [
        41428829,
        615064591,
        594226727,
        939719570,
    ]


def test_sort_ascending(client_operations):
    """reverse=False — возрастание: старые даты первыми."""
    result = sort_by_date(client_operations, reverse=False)

    assert [op["id"] for op in result] == [
        939719570,  # 2018-06-30
        594226727,  # 2018-09-12
        615064591,  # 2018-10-14
        41428829,  # 2019-07-03
    ]


def test_sort_same_dates(same_dates_operations):
    """Одинаковые даты → порядок сохраняется (stable sort)."""
    result = sort_by_date(same_dates_operations)

    assert [op["id"] for op in result] == [1, 2, 3]


def test_sort_same_dates_mixed():
    """Микс одинаковых и разных дат."""
    operations = [
        {"id": 1, "date": "2024-03-11T10:00:00.000000"},
        {"id": 2, "date": "2024-03-12T10:00:00.000000"},
        {"id": 3, "date": "2024-03-11T10:00:00.000000"},
    ]

    result = sort_by_date(operations)

    # 2024-03-12 — первым (новый).
    # Среди 2024-03-11: id=1, потом id=3 (порядок сохранён).
    assert [op["id"] for op in result] == [2, 1, 3]


def test_sort_empty():
    """Пустой список → пустой список."""
    assert sort_by_date([]) == []


def test_sort_single():
    """Один элемент → тот же список."""
    operations = [{"id": 1, "date": "2024-03-11T00:00:00.000000"}]
    assert sort_by_date(operations) == operations


def test_sort_does_not_mutate(client_operations):
    """Исходный список не меняется."""
    original = list(client_operations)
    sort_by_date(client_operations)
    assert client_operations == original


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [41428829, 615064591, 594226727, 939719570]),  # убывание
        (False, [939719570, 594226727, 615064591, 41428829]),  # возрастание
    ],
)
def test_sort_directions(client_operations, reverse, expected_ids):
    """Один тест — два направления сортировки."""
    result = sort_by_date(client_operations, reverse=reverse)
    assert [op["id"] for op in result] == expected_ids


@pytest.mark.parametrize(
    "operation",
    [
        {"id": 1},  # нет ключа date
        {"id": 2, "state": "EXECUTED"},  # нет ключа date
    ],
)
def test_sort_missing_date(operation):
    """Словарь без ключа date → KeyError."""
    with pytest.raises(KeyError):
        sort_by_date([operation])
