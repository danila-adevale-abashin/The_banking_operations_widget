import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_transaction_amount(transaction: dict) -> float:
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]
    if currency == "EUR":
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount={amount}"

        payload = {}
        headers = {"apikey": API_KEY}

        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()
        result = round(data["result"], 2)
        return result

    elif currency == "USD":
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount={amount}"

        payload = {}
        headers = {"apikey": API_KEY}

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code != 200:
            raise RuntimeError(f"API вернул {response.status_code}: {response.text}")

        data = response.json()
        result = round(data["result"], 2)
        return result

    else:
        return amount


if __name__ == "__main__":
    transaction = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": 31957.58, "currency": {"name": "руб.", "code": "RUB"}},
    }

    print(get_transaction_amount(transaction))
