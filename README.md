# Банковские операции

## Описание:

В данном проекте делается новая фича для личного кабинета клиента. 
Это виджет, который показывает несколько последних успешных банковских операций клиента.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/mrtimpr/PythonProject.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:

На текущий момент реализованны только отдельные функции виджета которые можно опробовать соответствующим вызовом:

- Из файла src/masks.py функция get_mask_card_number - принимает на вход номер карты и возвращает ее маску в формате XXXX XX** **** XXXX , где X — это цифра номера.

- Из файла src/masks.py функция get_mask_account - принимает на вход номер счета и возвращает его маску в формате **XXXX , где X— это цифра номера.

- Из файла src/widget.py функция mask_account_card - функция которая умеет обрабатывать информацию как о картах, так и о счетах. Возвращая строку с замаскированным номером.

- Из файла src/widget.py функция get_date - функция, которая принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407" и возвращает строку с датой в формате "ДД.ММ.ГГГГ"

- Из файла src/processing.py функция filter_by_state - принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED')

- Из файла src/processing.py функция sort_by_date - принимает список словарей и необязательный параметр сортировки

- Из файла src/generators.py функция filter_by_currency - принимает на вход список словарей, представляющих транзакции.

- Из файла src/generators.py функция transaction_descriptions - принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.

- Из файла src/generators.py функция card_number_generator - принимает начальное и конечное значения для генерации диапазона номеров.

- Из файла src/decorators.py функция log - Декоратор, логирующий начало и конец выполнения функции, результаты или ошибки в файл или консоль.

- Из файла src/utils.py функция load_transaction_data - принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях

- Из файла src/external_api.py функция convert_to_rub - принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float. Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли

- Из файла src/transactions_reader.py функция read_transactions_csv - Читает CSV-файл транзакций и возвращает список словарей.

- Из файла src/transactions_reader.py функция read_transactions_xlsx - Читает XLSX-файл (Excel) транзакций и возвращает список словарей.

- Из файла src/utils_for_data.py функция process_bank_search - Возвращает список словарей из data, у которых в поле 'description' встречается search (как подстрока, case-insensitive). Если search пустая строка -> возвращается пустой список.

- Из файла src/utils_for_data.py функция process_bank_operations - Возвращает словарь {категория: количество}, где для каждой категории считается, сколько операций в data имеют эту категорию как подстроку в поле 'description' (case-insensitive).

- Из файла main.py функция main - отвечает за основную логику проекта и связывает функциональности между собой.

## Примеры работ функций:

### для get_mask_card_number 

- Выход функции: `7000 79** **** 6361`

- Пример входных данных: `7000792289606361`

### для get_mask_account 

- Выход функции: `**4305`

- Пример входных данных: `73654108430135874305`

### для mask_account_card 

Примеры работы функции

- Пример для карты:
`Visa Platinum 7000792289606361  # входной аргумент
Visa Platinum 7000 79** **** 6361  # выход функции`

- Пример для счета:
`Счет 73654108430135874305  # входной аргумент
Счет **4305  # выход функции
Примеры входных данных для проверки функции
Maestro 1596837868705199
Счет 64686473678894779589
MasterCard 7158300734726758
Счет 35383033474447895560
Visa Classic 6831982476737658
Visa Platinum 8990922113665229
Visa Gold 5999414228426353
Счет 73654108430135874305`

### для get_date 

Примеры работы функции

- Выход функции: `11.03.2024`

- Пример входных данных: `2024-03-11T02:26:18.671407`

### для filter_by_state

Примеры работы функции
- Выход функции со статусом по умолчанию 'EXECUTED': 
`[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]`

- Выход функции, если вторым аргументов передано 'CANCELED': 
`[{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]`

- Пример входных данных для проверки функции: 
`[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]`

### для sort_by_date:

Примеры работы функции
- Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)
`[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]`

- Пример входных данных для проверки функции
`[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]`

### для filter_by_currency:

- Выход функции по фильтрации с указанием валюты "USD"
`[{
          "id": 939719570,
          "state": "EXECUTED",
          "date": "2018-06-30T02:08:58.425572",
          "operationAmount": {
              "amount": "9824.07",
              "currency": {
                  "name": "USD",
                  "code": "USD"
              }
          },
          "description": "Перевод организации",
          "from": "Счет 75106830613657916952",
          "to": "Счет 11776614605963066702"
      }
      {
              "id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
       }]`

- Пример входных данных для проверки функции
`[{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572", "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}, "description": "Перевод организации", "from": "Счет 75106830613657916952", "to": "Счет 11776614605963066702"}, {"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878", "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}}, "description": "Перевод со счета на счет", "from": "Счет 19708645243227258542", "to": "Счет 75651667383060284188"}, {"id": 873106923, "state": "EXECUTED", "date": "2019-03-23T01:09:46.296404", "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}}, "description": "Перевод со счета на счет", "from": "Счет 44812258784861134719", "to": "Счет 74489636417521191160"}, {"id": 895315941, "state": "EXECUTED", "date": "2018-08-19T04:27:37.904916", "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}}, "description": "Перевод с карты на карту", "from": "Visa Classic 6831982476737658", "to": "Visa Platinum 8990922113665229"}, { "id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689", "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}}, "description": "Перевод организации", "from": "Visa Platinum 1246377376343588", "to": "Счет 14211924144426031657"}]`

### для transaction_descriptions:

- Выход функции по выводу описаний каждой операции по очереди
```
Перевод организации
Перевод со счета на счет
Перевод со счета на счет
Перевод с карты на карту
Перевод организации
```
- Пример входных данных для проверки функции
`[{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572", "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}}, "description": "Перевод организации", "from": "Счет 75106830613657916952", "to": "Счет 11776614605963066702"}, {"id": 142264268, "state": "EXECUTED", "date": "2019-04-04T23:20:05.206878", "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}}, "description": "Перевод со счета на счет", "from": "Счет 19708645243227258542", "to": "Счет 75651667383060284188"}, {"id": 873106923, "state": "EXECUTED", "date": "2019-03-23T01:09:46.296404", "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}}, "description": "Перевод со счета на счет", "from": "Счет 44812258784861134719", "to": "Счет 74489636417521191160"}, {"id": 895315941, "state": "EXECUTED", "date": "2018-08-19T04:27:37.904916", "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}}, "description": "Перевод с карты на карту", "from": "Visa Classic 6831982476737658", "to": "Visa Platinum 8990922113665229"}, { "id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689", "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}}, "description": "Перевод организации", "from": "Visa Platinum 1246377376343588", "to": "Счет 14211924144426031657"}]`

### для card_number_generator:

- Выход функции с указанием диапазона генерации карт (1, 5):
```
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

### для декоратора log:

Пример использования декоратора

```
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
```

Ожидаемый вывод в лог-файл mylog.txt при успешном выполнении:

`my_function ok`

Ожидаемый вывод при ошибке:

`my_function error: тип ошибки. Inputs: (1, 2), {}`

Где тип ошибки заменяется на текст ошибки.

### для load_transaction_data:

Пример файла transactions.json:
```
[
  {
    "operationAmount": {
      "amount": "100.50",
      "currency": {
        "code": "RUB"
      }
    }
  },
  {
    "operationAmount": {
      "amount": "25.00",
      "currency": {
        "code": "USD"
      }
    }
  }
]
```

Ожидаемый вывод при выполнении кода:
```
Успешно загружено 2 транзакций.
Транзакция 1: 100.50 RUB
Транзакция 2: 25.00 USD
```

### для convert_to_rub:

```
# Пример транзакции в долларах
transaction_usd = {
    "operationAmount": {
        "amount": "100.50",
        "currency": {"code": "USD"}
    }
}

# Пример транзакции в рублях (конвертация не требуется)
transaction_rub = {
    "operationAmount": {
        "amount": "5000.00",
        "currency": {"code": "RUB"}
    }
}

# Используем функцию
amount_rub_usd = convert_to_rub(transaction_usd)
amount_rub_rub = convert_to_rub(transaction_rub)
amount_rub_bad = convert_to_rub({"bad": "data"}) # Пример с ошибкой

print(f"100.50 USD в RUB: {amount_rub_usd:.2f} RUB")
print(f"5000.00 RUB в RUB: {amount_rub_rub:.2f} RUB")
print(f"Результат для неверных данных: {amount_rub_bad}")
```

Ожидаемый вывод при выполнении кода:

#### (Точные значения курса могут меняться со временем)

```
100.50 USD в RUB: 9346.50 RUB
5000.00 RUB в RUB: 5000.00 RUB
Ошибка обработки входных данных: 'operationAmount'
Результат для неверных данных: 0.0
```

### для read_transactions_csv:

Предположим, у нас есть файл transactions.csv с таким содержимым:
csv
```
transaction_id,date,amount,description
1,2023-10-01,500.0,Groceries
2,2023-10-02,1200.5,Salary
3,2023-10-03,80.0,Coffee
```
Мы можем прочитать его, используя функцию read_transactions_csv
```
import src.transactions_reader as tr

file_path = "transactions.csv"

try:
    transactions_list = tr.read_transactions_csv(file_path)
    for transaction in transactions_list:
        print(f"ID: {transaction['transaction_id']}, Date: {transaction['date']}, Amount: {transaction['amount']}")

except FileNotFoundError:
    print(f"Ошибка: файл не найден по пути {file_path}")
except ValueError as e:
    print(f"Ошибка валидации данных: {e}")
```

Ожидаемый вывод при выполнении кода:

```
ID: 1, Date: 2023-10-01 00:00:00, Amount: 500.0
ID: 2, Date: 2023-10-02 00:00:00, Amount: 1200.5
ID: 3, Date: 2023-10-03 00:00:00, Amount: 80.0
```

### для read_transactions_csv:

Мы можем читать файлы Excel (.xlsx) и передавать дополнительные аргументы в базовую функцию Pandas (pd.read_excel), например, чтобы указать имя листа или дополнительные параметры парсинга.
```
transaction_id,date,amount,description
1,2023-10-01,500.0,Groceries
2,2023-10-02,1200.5,Salary
3,2023-10-03,80.0,Coffee
```
Мы можем прочитать его, используя функцию read_transactions_xlcx
```
import src.transactions_reader as tr
from pathlib import Path

# Пример чтения файла Excel, расположенного по пути Path
path_obj = Path("data_folder/my_transactions.xlsx")

try:
    # Указываем имя листа и опциональный параметр engine для pd.read_excel
    excel_data = tr.read_transactions_xlsx(
        path_obj, 
        sheet_name="October Data", 
        engine="openpyxl"
    )
    
    print(f"Успешно прочитано {len(excel_data)} транзакций из Excel.")

except Exception as e:
    print(f"Произошла ошибка при чтении Excel файла: {e}")
```

Ожидаемый вывод при выполнении кода:

```
ID: 1, Date: 2023-10-01 00:00:00, Amount: 500.0
ID: 2, Date: 2023-10-02 00:00:00, Amount: 1200.5
ID: 3, Date: 2023-10-03 00:00:00, Amount: 80.0
```
### для process_bank_search:
```
data = [
    {"id": 1, "description": "Оплата услуг мобильной связи"},
    {"id": 2, "description": "Покупка в магазине электроники"},
    {"id": 3, "description": "Перевод на карту: зарплата"},
    {"id": 4, "description": "Оплата услуг интернета"},
]
found = process_bank_search(data, "оплата")
print(found)
```
Ожидаемый вывод при выполнении кода:

`[{'id': 1, 'description': 'Оплата услуг мобильной связи'}, {'id': 4, 'description': 'Оплата услуг интернета'}]`


### для process_bank_operations:
```
data = [
    {"id": 1, "description": "Оплата услуг мобильной связи"},
    {"id": 2, "description": "Покупка в магазине электроники"},
    {"id": 3, "description": "Перевод на карту: зарплата"},
    {"id": 4, "description": "Оплата услуг интернета"},
]
categories = ["оплата", "покупка", "зарплата"]
counts = process_bank_operations(data, categories)
print(counts)
```

Ожидаемый вывод при выполнении кода: 

`{"оплата": 2, "покупка": 1, "зарплата": 1}`

### для main:

Ожидаемый вывод при выполнении кода: 

```
Программа: Привет! Добро пожаловать в программу работы 
с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла

Пользователь: 1

Программа: Для обработки выбран JSON-файл.

Программа: Введите статус, по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING

Пользователь: EXECUTED

Программа: Операции отфильтрованы по статусу "EXECUTED"

Программа: Отсортировать операции по дате? Да/Нет

Пользователь: да

Программа: Отсортировать по возрастанию или по убыванию? 

Пользователь: по убыванию

Программа: Выводить только рублевые транзакции? Да/Нет

Пользователь: да

Программа: Отфильтровать список транзакций по определенному слову 
в описании? Да/Нет

Пользователь: нет

Программа: Распечатываю итоговый список транзакций...

Программа: 
Всего банковских операций в выборке: 1

08.12.2019 Открытие вклада 
Счет **4321
Сумма: 40542 руб. 
```

## Тестирование

### Краткое описание

Проект использует фреймворк pytest для автоматизированного тестирования. Тесты расположены в директории tests/.

### Инструкции по запуску

#### Запуск всех тестов:
Перейдите в корневую директорию проекта в терминале. Выполните команду:
`pytest`

#### Запуск конкретного файла с тестами:
Перейдите в корневую директорию проекта. Выполните команду, указав путь к файлу:
`pytest tests/test_masks.py` or `pytest tests/test_widget.py` or `pytest tests/test_processing.py` or `pytest tests/test_generators.py` or `pytest tests/test_decorators.py`

#### Просмотр более подробной информации:
Для получения более детальной информации о выполнении тестов (например, о длительности выполнения) используйте флаг -v:
`pytest -v`

### Примеры тестов

#### Пример запуска и вывода tests/test_masks.py:

```
===== test session starts =====
collected 8 items
tests/test_masks.py ........                              [100%]
===== 8 passed in ...s =====
```

#### Пример запуска и вывода tests/test_widget.py:

```
===== test session starts =====
collected 8 items
tests/test_widget.py ........                               [100%]
===== 8 passed in ...s =====
```

#### Пример запуска и вывода tests/test_processing.py:

```
===== test session starts =====
collected 7 items
tests/test_processing.py .......                               [100%]
===== 7 passed in ...s =====
```

#### Пример запуска и вывода tests/test_generators.py:

```
===== test session starts =====
collected 10 items
tests/test_processing.py ..........                               [100%]
===== 10 passed in ...s =====
```

#### Пример запуска и вывода tests/test_decorators.py:

```
===== test session starts =====
collected 4 items
tests/test_decorators.py ....                               [100%]
===== 4 passed in ...s =====
```

#### Пример запуска и вывода tests/test_utils.py:

```
===== test session starts =====
collected 7 items
tests/test_utils.py .......                               [100%]
===== 7 passed in ...s =====
```

#### Пример запуска и вывода tests/test_external_api.py:

```
===== test session starts =====
collected 9 items
tests/test_external_api.py .........                               [100%]
===== 9 passed in ...s =====
```

#### Пример запуска и вывода tests/test_transactions_reader.py:

```
===== test session starts =====
collected 6 items
tests/test_external_api.py ......                               [100%]
===== 6 passed in ...s =====
```

#### Пример запуска и вывода tests/test_utils_for_data.py:

```
===== test session starts =====
collected 8 items
tests/test_utils_for_data.py ........                               [100%]
===== 8 passed in ...s =====
```

#### Пример запуска и вывода tests/test_main.py:

```
===== test session starts =====
collected 20 items
tests/test_utils_for_data.py ........                               [100%]
===== 20 passed in ...s =====
```

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).