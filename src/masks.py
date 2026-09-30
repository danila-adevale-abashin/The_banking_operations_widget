# IT-отдел крупного банка делает новую фичу для личного кабинета клиента. Это виджет,
# который показывает несколько последних успешных банковских операций клиента.
# Нам доверили реализовать этот проект, который на бэкенде будет готовить данные для отображения в новом виджете.


def get_mask_card_number(user_card_number: str) -> str:
    """Эта функция принимает номер банковской карты и возвращает его в замаскированном виде"""
    card_number = user_card_number.translate(str.maketrans('', '', ' -.'))
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    if not card_number.isdigit():
        raise ValueError('Номер карты должен содержать только цифры')


    mask_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:16]}"
    return mask_card_number


def get_mask_account(user_account: str) -> str:
    """Эта функция принимает номер банковского счета и возвращает номер в замаскированном виде"""
    account = user_account.translate(str.maketrans('', '', ' -.'))
    if len(account) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")
    if not account.isdigit():
        raise ValueError('Номер счета должен содержать только цифры')
    mask_account = f"**{account[-4:]}"
    return mask_account


if __name__ == "__main__":
    user_card_number = input("Введите номер Вашей банковской карты: ")
    user_account = input("\nВведите номер Вашего банковского счета: ")

    print(f"\nВаша банковская карта: {get_mask_card_number(user_card_number)}")

    print(f"\nВаш банковский счет: {get_mask_account(user_account)}")
