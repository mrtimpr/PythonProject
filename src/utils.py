import json
from pathlib import Path


def load_transaction_data(filepath: str) -> list[dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    path = Path(filepath)

    try:
        # Попытка открыть и прочитать файл.
        # Если файл не найден, будет сгенерирована FileNotFoundError.
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                print(f"Ошибка: Файл {filepath} пуст.")
                return []

            data = json.loads(content)

            if not isinstance(data, list):
                print(f"Ошибка: Содержимое файла {filepath} не является списком JSON.")
                return []

            return data

    except FileNotFoundError:
        # Специальная обработка для случая, когда файл не найден
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return []
    except json.JSONDecodeError:
        # Обработка ошибок парсинга JSON
        print(f"Ошибка: Не удалось декодировать JSON из файла {filepath}.")
        return []
    except Exception as e:
        # Обработка любых других непредвиденных ошибок
        print(f"Произошла непредвиденная ошибка при чтении файла: {e}")
        return []
