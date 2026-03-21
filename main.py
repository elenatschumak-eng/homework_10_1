from __future__ import annotations

from typing import Any

from src.data_readers import read_transactions_csv, read_transactions_excel
from src.utils import load_operations
from src.processing import filter_by_state, sort_by_date
from src.search_and_stats import process_bank_search, process_bank_operations


def _ask_choice() -> str:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    return input("Пользователь: ").strip()


def _load_transactions(choice: str) -> list[dict[str, Any]]:
    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        return load_operations("data/operations.json")
    if choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        return read_transactions_csv("data/transactions.csv")
    if choice == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
        return read_transactions_excel("data/transactions_excel.xlsx")

    print("Программа: Некорректный пункт меню.")
    return []


def _ask_state() -> str:
    allowed = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        state = input("Пользователь: ").strip().upper()
        if state in allowed:
            print(f'Программа: Операции отфильтрованы по статусу "{state}"')
            return state
        print(f'Программа: Статус операции "{state}" недоступен.')


def _ask_yes_no(prompt: str) -> bool:
    answer = input(prompt).strip().lower()
    return answer in {"да", "yes", "y", "д"}


def main() -> None:
    choice = _ask_choice()
    transactions = _load_transactions(choice)

    if not transactions:
        print("Программа: Нет данных для обработки.")
        return

    state = _ask_state()
    filtered = filter_by_state(transactions, state=state)

    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Sort questions
    if _ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: "):
        asc = _ask_yes_no(
            "Программа: Отсортировать по возрастанию или по убыванию?\n"
            "Пользователь (введите 'по возрастанию' / 'по убыванию'): "
        )
        # Wenn User "да" antwortet, interpretieren wir als "по возрастанию"
        # Einfach und robust: True => ascending
        reverse = not asc
        filtered = sort_by_date(filtered, reverse=reverse)

    # Optional: filter only RUB
    if _ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: "):
        only_rub: list[dict[str, Any]] = []
        for op in filtered:
            op_amount = op.get("operationAmount")
            if isinstance(op_amount, dict):
                cur = op_amount.get("currency")
                if isinstance(cur, dict) and cur.get("code") == "RUB":
                    only_rub.append(op)
        filtered = only_rub

    # Optional: search in description
    if _ask_yes_no(
        "Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
        "Пользователь: "
    ):
        search = input("Программа: Введите строку для поиска:\nПользователь: ").strip()
        filtered = process_bank_search(filtered, search)

    print("Программа: Распечатываю итоговый список транзакций...")
    print(f"Программа: Всего банковских операций в выборке: {len(filtered)}")

    # Optional: category stats
    if _ask_yes_no("Программа: Посчитать категории? Да/Нет\nПользователь: "):
        raw = input("Программа: Введите категории через запятую:\nПользователь: ").strip()
        categories = [c.strip() for c in raw.split(",") if c.strip()]
        stats = process_bank_operations(filtered, categories)
        print("Программа: Статистика по категориям:")
        for k, v in stats.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
