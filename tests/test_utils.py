import json
import pytest

from src.utils import get_operation_transactions


# --- ФИКСТУРЫ ДЛЯ СОЗДАНИЯ ВРЕМЕННЫХ ФАЙЛОВ ---

@pytest.fixture
def valid_json_file(tmp_path):
    """Создает временный валидный JSON-файл."""
    file = tmp_path / "valid.json"
    data = [
        {"id": 1, "amount": "100.0"},
        {"id": 2, "amount": "200.0"}
    ]
    file.write_text(json.dumps(data), encoding="utf-8")
    return str(file)


@pytest.fixture
def empty_json_file(tmp_path):
    """Создает временный пустой JSON-файл."""
    file = tmp_path / "empty.json"
    file.write_text("", encoding="utf-8")
    return str(file)


@pytest.fixture
def dict_json_file(tmp_path):
    """Создает файл, где внутри не список, а словарь."""
    file = tmp_path / "dict.json"
    file.write_text('{"key": "value"}', encoding="utf-8")
    return str(file)


@pytest.fixture
def broken_json_file(tmp_path):
    """Создает файл с битым (невалидным) JSON."""
    file = tmp_path / "broken.json"
    file.write_text('{"id": 1, "amount":', encoding="utf-8")
    return str(file)


# --- ТЕСТЫ ---

def test_get_operation_transactions_valid(valid_json_file):
    """Тест: читает нормальный список транзакций."""
    result = get_operation_transactions(valid_json_file)

    assert len(result) == 2
    assert isinstance(result, list)
    assert result[0]["id"] == 1


def test_get_operation_transactions_not_found(tmp_path):
    """Тест: если файла нет — возвращает []."""
    missing_file = str(tmp_path / "nonexistent.json")

    result = get_operation_transactions(missing_file)

    assert result == []


def test_get_operation_transactions_empty(empty_json_file, capsys):
    """Тест: пустой файл (0 байт) — возвращает []."""
    result = get_operation_transactions(empty_json_file)

    assert result == []

    captured = capsys.readouterr()
    assert "Поймана ошибка: JSONDecodeError" in captured.out


def test_get_operation_transactions_not_a_list(dict_json_file, capsys):
    """Тест: если JSON — это словарь, а не список — возвращает []."""
    result = get_operation_transactions(dict_json_file)

    assert result == []

    captured = capsys.readouterr()
    assert "Данные не являются списком!" in captured.out


def test_get_operation_transactions_broken(broken_json_file, capsys):
    """Тест: если JSON битый — возвращает []."""
    result = get_operation_transactions(broken_json_file)

    assert result == []

    captured = capsys.readouterr()
    assert "Поймана ошибка: JSONDecodeError" in captured.out