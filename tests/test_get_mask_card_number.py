import pytest

from src.masks import get_mask_card_number

@pytest.fixture
def correct_card_number():
    return {'card': '2200000000000004', 'expected': '2200 00** **** 0004'}


def test_correct_result(correct_card_number):
    assert get_mask_card_number(correct_card_number['card']) == correct_card_number['expected']


@pytest.mark.parametrize('card_number', [
    '',                                  # пустая
    '123549',                            # короче
    '123456789012345',                   # 15 цифр
    '12345678901234567',                 # 17 цифр
    '123151498412106541984512631984211', # сильно длиннее
    'abcdefghijklmnop',                  # нецифры
])


def test_exception_result(card_number):
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)