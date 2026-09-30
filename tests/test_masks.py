import pytest

from src.masks import get_mask_account, get_mask_card_number

# 1. Тесты для функции get_mask_card_number:


@pytest.fixture
def correct_card_number():
    return {"card": "2200000000000004", "expected": "2200 00** **** 0004"}


def test_correct_result(correct_card_number):
    assert get_mask_card_number(correct_card_number["card"]) == correct_card_number["expected"]


@pytest.mark.parametrize(
    "card_number",
    [
        "",  # пустая
        "123549",  # короче
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
        "123151498412106541984512631984211",  # сильно длиннее
        "abcdefghijklmnop",  # не цифры
    ],
)
def test_exception_result(card_number):
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


# 2. Тесты для функции get_mask_account:

# @pytest.fixture
# def correct_account_number():
#     return {'account': '12345678912345678912', 'expected': '**8912'}
#
#
# def test_correct_account(correct_account_number):
#     assert get_mask_account(correct_account_number['account']) == correct_account_number['expected']


@pytest.mark.parametrize(
    "account, expected",
    [
        ("12345678912345678912", "**8912"),
        ("1234 5678 9123 4567 8912", "**8912"),
        ("12 34    56 7891 234 567 89 12", "**8912"),
    ],
)
def test_correct_account(account, expected):
    assert get_mask_account(account) == expected


@pytest.mark.parametrize(
    "account",
    [
        "",  # пустая
        "123549",  # короче
        "1234567891234567891",  # 19 цифр
        "123456789123056789123",  # 21 цифр
        "123151498412106541984512631456984211",  # сильно длиннее
        "asdfghsdfsfsdffffjkl",  # не цифры
    ],
)
def test_exception_account(account):
    with pytest.raises(ValueError):
        get_mask_account(account)
