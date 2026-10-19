import functools


def log(filename=None):
    """Декоратор логирует автоматически начало и конец выполнения функции,
    а также её результаты или возникшие ошибки"""

    def my_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{function.__name__} ok\n")
                else:
                    print(f"{function.__name__} ok\n")

                return result

            except Exception as e:
                error_message = f"{function.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{error_message}\n")
                else:
                    print(f"{error_message}\n")

                raise

        return wrapper

    return my_decorator


if __name__ == "__main__":

    @log()
    def get_mask_card_number(user_card_number) -> str:
        """Эта функция принимает номер банковской карты и возвращает его в замаскированном виде"""
        card_number = user_card_number.translate(str.maketrans("", "", " -."))
        if len(card_number) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        if not card_number.isdigit():
            raise ValueError("Номер карты должен содержать только цифры")

        mask_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:16]}"
        return mask_card_number

    print(get_mask_card_number(1234567891234567))

    def test_log():
        @log
        def get_mask_card_number(user_card_number=1234567891234567) -> str:
            """Эта функция принимает номер банковской карты и возвращает его в замаскированном виде"""
            card_number = user_card_number.translate(str.maketrans("", "", " -."))
            if len(card_number) != 16:
                raise ValueError("Номер карты должен содержать 16 цифр")
            if not card_number.isdigit():
                raise ValueError("Номер карты должен содержать только цифры")

            mask_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:16]}"
            return mask_card_number

        result = get_mask_card_number(1234567891234569)
        assert result
