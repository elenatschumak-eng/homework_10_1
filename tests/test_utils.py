import json
from pathlib import Path

from src.utils import load_operations


def test_load_operations_file_not_found(tmp_path: Path) -> None:
    missing = tmp_path / "missing.json"
    assert load_operations(missing) == []


def test_load_operations_empty_file(tmp_path: Path) -> None:
    p = tmp_path / "empty.json"
    p.write_text("", encoding="utf-8")
    assert load_operations(p) == []


def test_load_operations_not_a_list(tmp_path: Path) -> None:
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert load_operations(p) == []


def test_load_operations_list_with_non_dict_items(tmp_path: Path) -> None:
    p = tmp_path / "data.json"
    p.write_text(json.dumps([{"id": 1}, "bad", 123, {"id": 2}]), encoding="utf-8")
    result = load_operations(p)
    assert result == [{"id": 1}, {"id": 2}]
