from __future__ import annotations

from typing import Any

from src.data_readers import read_transactions_csv, read_transactions_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.search_and_stats import process_bank_operations, process_bank_search
from src.utils import load_operations
from src.widget import get_date, mask_account_card


def _ask_choice() -> str:
    """Ask the user to select the data source (JSON/CSV/XLSX)."""
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice in {"1", "2", "3"}:
            return choice
        print("Программа: Некорректный пункт меню. Попробуйте ещё раз.")


def _load_transactions(choice: str) -> list[dict[str, Any]]:
    """Load transactions based on the chosen source."""
    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        return load_operations("data/operations.json")
    if choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        return read_transactions_csv("data/transactions.csv")
    # choice == "3"
    print("Программа: Для обработки выбран XLSX-файл.")
    return read_transactions_excel("data/transactions_excel.xlsx")


def _ask_state() -> str:
    """Ask for a valid transaction state and normalize it to upper-case."""
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
    """Ask a yes/no question and return True for 'yes' answers."""
    answer = input(prompt).strip().lower()
    return answer in {"да", "д", "yes", "y"}


def _ask_sort_reverse() -> bool:
    """Ask sort order and return reverse flag for sort_by_date (True = descending)."""
    print("Программа: Отсортировать по возрастанию или по убыванию?")
    print("Пользователь (введите 'по возрастанию' / 'по убыванию'):")

    while True:
        raw = input("Пользователь: ").strip().lower()
        if "возрастан" in raw:
            return False  # ascending => reverse=False
        if "убыв" in raw:
            return True  # descending => reverse=True
        print("Программа: Введите 'по возрастанию' или 'по убыванию'.")


def _format_currency_label(code: str) -> str:
    """Format currency code for output."""
    if code == "RUB":
        return "руб."
    return code


def _safe_mask(value: Any) -> str:
    """Try to mask account/card string using mask_account_card; fallback to string."""
    if not isinstance(value, str) or not value.strip():
        return ""
    try:
        return mask_account_card(value)
    except Exception:
        return value


def _format_operation(op: dict[str, Any]) -> str:
    """Format a single operation dict into a human-readable multi-line string."""
    # date
    date_raw = op.get("date")
    date_str = ""
    if isinstance(date_raw, str) and date_raw.strip():
        try:
            date_str = get_date(date_raw)
        except ValueError:
            date_str = date_raw

    # description
    desc = op.get("description")
    desc_str = desc if isinstance(desc, str) else "Без описания"

    # from/to
    from_part = _safe_mask(op.get("from"))
    to_part = _safe_mask(op.get("to"))

    # amount + currency
    amount_line = ""
    op_amount = op.get("operationAmount")
    if isinstance(op_amount, dict):
        amount_raw = op_amount.get("amount")
        cur = op_amount.get("currency")

        code = ""
        if isinstance(cur, dict):
            code_val = cur.get("code")
            if isinstance(code_val, str):
                code = code_val

        if isinstance(amount_raw, str) and amount_raw.strip() and code:
            amount_line = f"Сумма: {amount_raw} {_format_currency_label(code)}"

    lines: list[str] = []
    if date_str:
        lines.append(f"{date_str} {desc_str}")
    else:
        lines.append(desc_str)

    if from_part and to_part:
        lines.append(f"{from_part} -> {to_part}")
    elif to_part:
        lines.append(to_part)
    elif from_part:
        lines.append(from_part)

    if amount_line:
        lines.append(amount_line)

    return "\n".join(lines)


def main() -> None:
    """Run the console program to filter and display banking transactions."""
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

    # Sort by date?
    if _ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: "):
        reverse = _ask_sort_reverse()
        filtered = sort_by_date(filtered, reverse=reverse)

    # Only RUB?
    if _ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: "):
        filtered = list(filter_by_currency(filtered, "RUB"))

    # Search in description?
    if _ask_yes_no(
        "Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
        "Пользователь: "
    ):
        search = input("Программа: Введите строку для поиска:\nПользователь: ").strip()
        filtered = process_bank_search(filtered, search)

    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Программа: Распечатываю итоговый список транзакций...")
    print(f"Программа: Всего банковских операций в выборке: {len(filtered)}")
    print()

    for op in filtered:
        if isinstance(op, dict):
            print(_format_operation(op))
            print()

    # Category stats?
    if _ask_yes_no("Программа: Посчитать категории? Да/Нет\nПользователь: "):
        raw = input("Программа: Введите категории через запятую:\nПользователь: ").strip()
        categories = [c.strip() for c in raw.split(",") if c.strip()]
        stats = process_bank_operations(filtered, categories)

        print("Программа: Статистика по категориям:")
        for cat in categories:
            print(f"{cat}: {stats.get(cat, 0)}")


if __name__ == "__main__":
    main()
