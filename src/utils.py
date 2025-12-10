import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="utils.log",  # Запись логов в файл
    filemode="w",
)  # Перезапись файла при каждом запуске
logger = logging.getLogger("utils")


def load_transaction_data(filepath: str) -> list[dict]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.
    """
    path = Path(filepath)
    logger.debug(f"Попытка загрузить данные из файла: {path.resolve()}")

    try:
        # Попытка открыть и прочитать файл.
        # Если файл не найден, будет сгенерирована FileNotFoundError.
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            logger.debug("Файл успешно открыт и прочитан.")

            if not content:
                logger.warning(f"Файл {filepath} пуст.")
                return []

            data = json.loads(content)
            logger.info(f"Данные из файла {filepath} успешно декодированы из JSON.")

            if not isinstance(data, list):
                logger.error(
                    f"Ошибка: Содержимое файла {filepath} не является списком JSON. Получен тип: {type(data).__name__}"
                )
                return []

            logger.info(f"Успешно загружено {len(data)} транзакций.")
            return data

    except FileNotFoundError:
        # Специальная обработка для случая, когда файл не найден
        logger.error(f"Ошибка: Файл не найден по пути {path.resolve()}", exc_info=True)
        return []
    except json.JSONDecodeError as e:
        # Обработка ошибок парсинга JSON
        logger.error(f"Ошибка декодирования JSON в файле {filepath}: {e}", exc_info=True)
        return []
    except Exception as e:
        # Обработка любых других непредвиденных ошибок
        logger.critical(f"Произошла непредвиденная ошибка при чтении файла {filepath}: {e}", exc_info=True)
        return []
