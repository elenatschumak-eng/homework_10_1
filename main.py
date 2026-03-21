from __future__ import annotations

from pathlib import Path
from typing import Any

from src.data_readers import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, sort_by_date
from src.utils import load_operations
from src.widget import get_date, mask_account_card

# Passe den Import an, falls deine Datei anders heißt:
# z.B. src/search_and_stats.py oder src/search_and_stats_functions.py
from src.search_and_stats import process_bank_search

Operation = dict[str, Any]


DATA_DIR = Path("data")
JSON_PATH = DATA_DIR / "operations.json"
CSV_PATH = DATA_DIR / "transactions.csv"
XLSX_PATH = DATA_DIR / "transactions_excel.xlsx"

ALLOWED_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def _ask_menu_choice() -> int:
    while True:
        raw = input("Пользователь: ").strip()
        if raw in {"1", "2", "3"}:
            return int(raw)
        print("Программа: Пожалуйста, введите 1, 2 или 3.")


def _ask_yes_no(prompt_text: str) -> bool:
    """Return True for 'да', False for 'нет'. Keeps asking until valid."""
    while True:
        print(f"Программа: {prompt_text}")
        raw = input("Пользователь: ").strip().lower()
        if raw in {"да", "д", "y", "yes"}:
            return True
        if raw in {"нет", "н", "n", "no"}:
            return False
        print("Программа: Ответьте 'Да' или 'Нет'.")


def _ask_status() -> str:
    while True:
        print(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        raw = input("Пользователь: ").strip().upper()
        if raw in ALLOWED_STATUSES:
            print(f'Программа: Операции отфильтрованы по статусу "{raw}"')
            return raw
        print(f'Программа: Статус операции "{raw}" недоступен.')


def _ask_sort_order() -> bool:
    """Return reverse flag for sort_by_date: True = descending, False = ascending."""
    while True:
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        raw = input("Пользователь: ").strip().lower()

        if "возрастан" in raw:
            return False
        if "убыван" in raw:
            return True

        print("Программа: Введите 'по возрастанию' или 'по убыванию'.")


def _is_rub_operation(op: Operation) -> bool:
    op_amount = op.get("operationAmount")
    if not isinstance(op_amount, dict):
        return False
    cur = op_amount.get("currency")
    if not isinstance(cur, dict):
        return False
    code = cur.get("code")
    return isinstance(code, str) and code.upper() == "RUB"


def _format_operation(op: Operation) -> list[str]:
    # Date + description
    date_raw = op.get("date")
    desc = op.get("description")

    date_str = str(date_raw) if date_raw is not None else ""
    if isinstance(date_raw, str):
        try:
            date_str = get_date(date_raw)
        except ValueError:
            date_str = date_raw

    desc_str = desc if isinstance(desc, str) else ""

    lines: list[str] = [f"{date_str} {desc_str}".strip()]

    # From/To
    from_ = op.get("from")
    to_ = op.get("to")

    from_str = from_ if isinstance(from_, str) else ""
    to_str = to_ if isinstance(to_, str) else ""

    if from_str and to_str:
        lines.append(f"{mask_account_card(from_str)} -> {mask_account_card(to_str)}")
    elif to_str:
        lines.append(mask_account_card(to_str))
    elif from_str:
        lines.append(mask_account_card(from_str))

    # Amount + currency
    op_amount = op.get("operationAmount")
    amount_out = "-"
    currency_out = ""

    if isinstance(op_amount, dict):
        amount = op_amount.get("amount")
        cur = op_amount.get("currency")

        if isinstance(amount, str):
            amount_out = amount
        elif isinstance(amount, (int, float)):
            amount_out = str(amount)

        if isinstance(cur, dict):
            code = cur.get("code")
            if isinstance(code, str):
                currency_out = "руб." if code.upper() == "RUB" else code.upper()

    if currency_out:
        lines.append(f"Сумма: {amount_out} {currency_out}")
    else:
        lines.append(f"Сумма: {amount_out}")

    return lines


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Программа: Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = _ask_menu_choice()

    if choice == 1:
        print("Программа: Для обработки выбран JSON-файл.")
        operations = load_operations(JSON_PATH)
    elif choice == 2:
        print("Программа: Для обработки выбран CSV-файл.")
        operations = read_transactions_csv(CSV_PATH)
    else:
        print("Программа: Для обработки выбран XLSX-файл.")
        operations = read_transactions_excel(XLSX_PATH)

    status = _ask_status()
    operations = filter_by_state(operations, status)

    if _ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        reverse = _ask_sort_order()
        operations = sort_by_date(operations, reverse=reverse)

    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        operations = [op for op in operations if _is_rub_operation(op)]

    if _ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        print("Программа: Введите строку для поиска в описании:")
        search = input("Пользователь: ").strip()
        operations = process_bank_search(operations, search)

    if not operations:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Программа: Распечатываю итоговый список транзакций...")
    print(f"Программа:\nВсего банковских операций в выборке: {len(operations)}\n")

    for op in operations:
        for line in _format_operation(op):
            print(line)
        print()  # empty line between operations


if __name__ == "__main__":
    main()
