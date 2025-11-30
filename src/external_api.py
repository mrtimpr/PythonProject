import os
from typing import Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout

# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменной API_KEY из .env-файла
API_KEY: Optional[str] = os.getenv("API_KEY")

# Проверяем ключ сразу при старте скрипта
if not API_KEY:
    print("Внимание: Переменная окружения API_KEY не найдена или пуста.")


def convert_to_rub(transaction: dict) -> Optional[float]:
    """Функция осуществляет конвертацию суммы транзакции в рубли.
    Возвращает сумму в RUB в виде float или None в случае ошибки."""

    try:
        amount_str = transaction["operationAmount"]["amount"]
        amount = float(amount_str)
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            return amount

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": API_KEY}

        response = requests.get(url, headers=headers, timeout=5)

        response.raise_for_status()

        result = response.json()

        if "result" in result:
            return float(result["result"])
        else:
            print(f"Ошибка API: Неожиданный формат ответа: {result}")
            return 0.0

    except (KeyError, ValueError) as e:
        print(f"Ошибка обработки входных данных: {e}")
        return 0.0
    except HTTPError as e:
        print(f"Ошибка HTTP запроса (клиентская или серверная): {e}")
        return 0.0
    except ConnectionError as e:
        print(f"Ошибка подключения к сети: {e}")
        return 0.0
    except Timeout as e:
        print(f"Превышено время ожидания ответа от API: {e}")
        return 0.0
    except RequestException as e:
        print(f"Неизвестная ошибка запроса: {e}")
        return 0.0
