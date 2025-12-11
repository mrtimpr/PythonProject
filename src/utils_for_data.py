import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Возвращает список словарей из data, у которых в поле 'description' встречается search (как подстрока,
    case-insensitive). Если search пустая строка -> возвращается пустой список.
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result: List[Dict[str, Any]] = []
    for item in data:
        desc = item.get("description", "")
        if isinstance(desc, str) and pattern.search(desc):
            result.append(item)
    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Возвращает словарь {категория: количество}, где для каждой категории считается,
    сколько операций в data имеют эту категорию как подстроку в поле 'description' (case-insensitive),
    используя collections.Counter.
    """
    counts = Counter({cat: 0 for cat in categories})

    patterns = {cat: re.compile(re.escape(cat), re.IGNORECASE) for cat in categories}

    for item in data:
        desc = item.get("description", "")
        if not isinstance(desc, str):
            continue
        for cat, pat in patterns.items():
            if pat.search(desc):
                counts[cat] += 1

    return dict(counts)
