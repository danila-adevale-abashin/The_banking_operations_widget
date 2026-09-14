# IT-отдел крупного банка делает новую фичу для личного кабинета клиента. Это виджет,
# который показывает несколько последних успешных банковских операций клиента.
# Нам доверили реализовать этот проект, который на бэкенде будет готовить данные для отображения в новом виджете.

user_card_number = input("Введите номер Вашей банковской карты: ")
user_account = input("\nВведите номер Вашего банковского счета: ")


def get_mask_card_number(user_card_number: str) -> str:
    """Эта функция принимает номер банковской карты и возвращает его в замаскированном виде"""
    if len(user_card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    mask_card_number = f"{user_card_number[:4]} {user_card_number[4:6]}** **** {user_card_number[12:16]}"
    return mask_card_number


print(f"\nВаша банковская карта: {get_mask_card_number(user_card_number)}")


def get_mask_account(user_account: str) -> str:
    """Эта функция принимает номер банковского счета и возвращает номер в замаскированном виде"""
    if len(user_account) != 20:
        raise ValueError("Номер счета должен содержать 20 цифр")
    mask_account = f"**{user_account[-4:]}"
    return mask_account


print(f"\nВаш банковский счет: {get_mask_account(user_account)}")
