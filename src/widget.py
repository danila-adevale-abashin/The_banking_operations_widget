user_account_card = input("Введите информацио о карте/счете и укажите её/его номер: ")


def mask_account_card(account_card: str) -> str:
    """
    Функция принимает в себя информацию о карте/счете и маскирует, выдавая ту же информацию, но с маской
    :param account_card: Введённая пользователем информация и номер о карте/счете
    :return: Информация о карте/счете с маской
    """
    # Создаем две строки, в которые поместим отдельно номер и инфу с табуляцией
    is_number = ""
    is_not_number = ""
    for symbol in account_card:
        if symbol.isdigit():
            is_number = is_number + symbol
        else:
            is_not_number = is_not_number + symbol
    # Если длина строки номера - 16, маскируем как карту
    if len(is_number) == 16:
        return f"{is_not_number}{is_number[:4]} {is_number[4:6]}** **** {is_number[12:16]}"
    # Если длина номера - 20, маскируем как счет
    elif len(is_number) == 20:
        return f"{is_not_number}**{is_number[-4:]}"
    else:
        raise ValueError("Номер карты должен содержать 16 цифр. Номер счета - 20 цифр")


print(f"\n{mask_account_card(user_account_card)}")
