import pytest

from src.widget import get_date, mask_account_card

# 1. Тесты для функции mask_account_card:


@pytest.mark.parametrize(
    "card_or_account_info, expected",
    [
        ("VisaCard 1234567891234567", "VisaCard 1234 56** **** 4567"),
        ("MasterCard 1234 3678 9123 4567", "MasterCard 1234 36** **** 4567"),
        ("MasterCard 12347651212345678910", "MasterCard **8910"),
        ("MasterCard 1234 5678 9123 4567 9012", "MasterCard **9012"),
    ],
)
def test_valid_mask_account_card(card_or_account_info, expected):
    assert mask_account_card(card_or_account_info) == expected


@pytest.mark.parametrize(
    "card_or_account_info",
    [
        (""),  # Пустой ввод
        ("МИР"),  # Только текст
        ("VisaCard 123"),  # Маленький номер
        ("VisaCard 123456789123456"),  # Номер из 15 цифр
        ("VisaCard 12345678912345678"),  # Номер из 17 цифр
        ("MasterCard 1234567891234567891"),  # Счет из 19 цифр
        ("MasterCard 123456789123456789123"),  # Счет из 21 цифры
        ("MasterCard 123456789123456789128748941654689156165"),  # Очень много цифр
    ],
)
def test_exception_result(card_or_account_info):
    with pytest.raises(ValueError):
        mask_account_card(card_or_account_info)


# 2. Тесты для функции get_date:


@pytest.mark.parametrize(
    "iso_string, expected",
    [
        ("2024-03-11", "11.03.2024"),  # только дата
        ("2024-03-11T02:26:18", "11.03.2024"),  # дата + время
        ("2024-03-11T02:26:18.671407", "11.03.2024"),  # с микросекундами
        ("2024-03-11T02:26:18+03:00", "11.03.2024"),  # с таймзоной
        ("2024-03-11T02:26:18Z", "11.03.2024"),  # UTC (Z)
        ("2024-03-11 02:26:18", "11.03.2024"),  # пробел вместо T
    ],
)
def test_correct_date(iso_string, expected):
    assert get_date(iso_string) == expected


@pytest.mark.parametrize(
    "iso_string, expected",
    [
        ("2024-01-01T00:00:00", "01.01.2024"),  # начало года
        ("2024-12-31T23:59:59", "31.12.2024"),  # конец года
        ("2024-02-29T12:00:00", "29.02.2024"),  # високосный
        ("2023-02-28T12:00:00", "28.02.2023"),  # невисокосный
    ],
)
def test_boundary_dates(iso_string, expected):
    assert get_date(iso_string) == expected


@pytest.mark.parametrize(
    "invalid_string",
    [
        "",  # пустая
        "   ",  # пробелы
        "not a date",  # текст
        "2024/03/11",  # не ISO (слэши)
        "11.03.2024",  # уже форматированная
        "2024-13-01",  # месяц 13 — не бывает
        "2024-02-30",  # 30 февраля — не бывает
        "2024-03",  # только год и месяц
        "2024",  # только год
    ],
)
def test_invalid_date(invalid_string):
    with pytest.raises(ValueError):
        get_date(invalid_string)
