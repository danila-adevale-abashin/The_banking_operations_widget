from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.file_readers import get_transactions_from_csv, get_transactions_from_excel

# --- ТЕСТЫ ДЛЯ CSV ---


@patch("src.file_readers.pd.read_csv")
def test_get_transactions_from_csv_success(mock_read_csv):
    """Тест: успешное чтение CSV"""

    fake_df = pd.DataFrame(
        [{"id": 1, "amount": 100.0, "currency": "RUB"}, {"id": 2, "amount": 200.0, "currency": "USD"}]
    )

    mock_read_csv.return_value = fake_df

    result = get_transactions_from_csv("fake_path.csv")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["currency"] == "USD"

    mock_read_csv.assert_called_once_with("fake_path.csv")


@patch("src.file_readers.pd.read_csv")
def test_get_transactions_from_csv_error(mock_read_csv):
    """Тест: если read_csv падает с ошибкой, функция возвращает []"""

    mock_read_csv.side_effect = Exception("Файл не найден")

    result = get_transactions_from_csv("broken_path.csv")

    assert result == []
    mock_read_csv.assert_called_once()


# --- ТЕСТЫ ДЛЯ EXCEL ---


@patch("src.file_readers.pd.read_excel")
def test_get_transactions_from_excel_success(mock_read_excel):
    """Тест: успешное чтение Excel"""
    fake_df = pd.DataFrame([{"id": 3, "amount": 300.0, "currency": "EUR"}])
    mock_read_excel.return_value = fake_df

    result = get_transactions_from_excel("fake_path.xlsx")

    assert len(result) == 1
    assert result[0]["id"] == 3
    mock_read_excel.assert_called_once_with("fake_path.xlsx")


@patch("src.file_readers.pd.read_excel")
def test_get_transactions_from_excel_error(mock_read_excel):
    """Тест: если read_excel падает, функция возвращает []"""
    mock_read_excel.side_effect = Exception("Ошибка Excel")

    result = get_transactions_from_excel("broken_path.xlsx")

    assert result == []
