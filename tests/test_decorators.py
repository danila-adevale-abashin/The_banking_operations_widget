import pytest

from src.decorators import log

# ===== ТЕСТ 1: успех в консоль =====


def test_log_success_console(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(1, 2)

    captured = capsys.readouterr()
    assert result == 3
    assert captured.out == "add ok\n\n"
    assert captured.err == ""


# ===== ТЕСТ 2: ошибка в консоль =====


def test_log_error_console(capsys):
    @log()
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    captured = capsys.readouterr()
    assert "div error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


# ===== ТЕСТ 3: успех в файл =====


def test_log_success_file(tmp_path):
    file = tmp_path / "mylog.txt"

    @log(filename=str(file))
    def add(a, b):
        return a + b

    result = add(1, 2)

    assert result == 3
    assert file.read_text(encoding="utf-8") == "add ok\n"


# ===== ТЕСТ 4: ошибка в файл =====


def test_log_error_file(tmp_path):
    file = tmp_path / "mylog.txt"

    @log(filename=str(file))
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(1, 0)

    content = file.read_text(encoding="utf-8")
    assert "div error: ZeroDivisionError" in content
    assert "Inputs: (1, 0), {}" in content


# ===== ТЕСТ 5: kwargs в логе =====


def test_log_kwargs(capsys):
    @log()
    def greet(name, greeting="Привет"):
        return f"{greeting}, {name}!"

    with pytest.raises(ValueError):

        @log()
        def fail(a, b, *, c):
            raise ValueError("boom")

        fail(1, 2, c=3)

    captured = capsys.readouterr()
    assert "Inputs: (1, 2), {'c': 3}" in captured.out


# ===== ТЕСТ 6: результат возвращается из обёртки =====


def test_log_returns_result(capsys):
    @log()
    def multiply(a, b):
        return a * b

    assert multiply(3, 4) == 12
    captured = capsys.readouterr()
    assert captured.out == "multiply ok\n\n"


# ===== ТЕСТ 7: исключение пробрасывается =====


def test_log_reraises_exception(capsys):
    @log()
    def always_fails():
        raise ValueError("always")

    with pytest.raises(ValueError, match="always"):
        always_fails()
