from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


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
    info_about_number = is_not_number.translate(str.maketrans("", "", " "))
    # Если длина строки номера - 16, маскируем как карту
    if len(is_number) == 16:
        return f"{info_about_number} {get_mask_card_number(is_number)}".strip()
    # Если длина номера - 20, маскируем как счет
    elif len(is_number) == 20:
        return f"{info_about_number} {get_mask_account(is_number)}".strip()
    else:
        raise ValueError("Номер карты должен содержать 16 цифр. Номер счета - 20 цифр")


def get_date(date_info: str) -> str:
    """
    Функция принимает определенный формат даты, выводя дату в формате "ДД.ММ.ГГГГ"
    :param date_info: Дата определенного формата
    :return: Отредактированная дата
    """
    iso_date = datetime.fromisoformat(date_info)
    result_date = iso_date.strftime("%d.%m.%Y")
    return result_date


if __name__ == "__main__":
    user_account_card = input("Введите информацию о карте/счете и укажите её/его номер: ")

    print(f"\n{mask_account_card(user_account_card)}")

    print(get_date("2024-03-11T02:26:18.671407"))
