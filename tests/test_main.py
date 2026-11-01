import pytest
from unittest.mock import patch
from src.main import main


@patch('builtins.print')
def test_main_json_success(mock_print, monkeypatch):
    """Тест: успешный проход main() с выбором JSON."""

    inputs = iter(['1', 'EXECUTED', 'нет', 'нет', 'нет'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('src.main.get_operation_transactions') as mock_get:
        mock_get.return_value = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB", "name": "руб."}},
                "description": "Перевод",
                "from": "Счет 12345678901234567890",
                "to": "Счет 09876543210987654321"
            }
        ]

        main()

        mock_print.assert_any_call("Распечатываю итоговый список транзакций...\nВсего банковских операций в выборке: 1")


@patch('builtins.print')
def test_main_invalid_choice(mock_print, monkeypatch):
    """Тест: проверка неверного выбора меню."""
    monkeypatch.setattr('builtins.input', lambda _: '99')

    main()

    mock_print.assert_any_call("Неверный выбор. Попробуйте ещё раз.")


@patch('builtins.print')
def test_main_empty_transactions(mock_print, monkeypatch):
    """Тест: проверка случая, когда после фильтрации ничего не осталось."""
    inputs = iter(['1', 'PENDING', 'нет', 'нет', 'нет'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('src.main.get_operation_transactions') as mock_get:
        mock_get.return_value = []  # пустой список

        main()

        mock_print.assert_any_call("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")