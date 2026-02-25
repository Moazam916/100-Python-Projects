import json
import pandas as pd
import pytest
from main import get_columns_from_csv, highlight_columns, lambda_handler


def make_csv(tmp_path, columns, rows=None):
    """Helper to create a CSV file with given columns and optional rows."""
    data = {col: [] for col in columns}
    if rows:
        for row in rows:
            for col in columns:
                data[col].append(row.get(col, ""))
    df = pd.DataFrame(data)
    path = tmp_path / "test.csv"
    df.to_csv(path, index=False)
    return str(path)


def test_get_columns_from_csv(tmp_path):
    cols = ["a", "b", "c"]
    csv_file = make_csv(tmp_path, cols)
    result = get_columns_from_csv(csv_file)
    assert result == cols


def test_get_columns_from_csv_with_nrows(tmp_path):
    cols = ["a", "b", "c"]
    # create a CSV with 50 rows
    rows = [{"a": str(i), "b": str(i * 2), "c": str(i * 3)} for i in range(50)]
    data = {col: [] for col in cols}
    for row in rows:
        for col in cols:
            data[col].append(row[col])
    df = pd.DataFrame(data)
    path = tmp_path / "test_large.csv"
    df.to_csv(path, index=False)
    
    # load with nrows=10, columns should still be the same
    result = get_columns_from_csv(str(path), nrows=10)
    assert result == cols


def test_highlight_columns_no_query():
    cols = ["foo", "bar"]
    highlighted, matches = highlight_columns(cols, None)
    assert highlighted == cols
    assert matches == []


def test_highlight_columns_substring():
    cols = ["first", "second", "third"]
    highlighted, matches = highlight_columns(cols, "ir", exact=False)
    # substring search matches "first" and "third"
    assert highlighted == ["\x1b[31mfirst\x1b[0m", "second", "\x1b[31mthird\x1b[0m"]
    assert matches == ["first", "third"]


def test_highlight_columns_exact():
    cols = ["id", "customer_id", "order_id"]
    highlighted, matches = highlight_columns(cols, "id", exact=True)
    # exact match only highlights the lone "id"
    assert highlighted == ["\x1b[31mid\x1b[0m", "customer_id", "order_id"]
    assert matches == ["id"]


def test_lambda_handler_missing_path():
    event = {}
    resp = lambda_handler(event, None)
    assert "error" in resp


def test_lambda_handler_with_search(tmp_path):
    cols = ["x", "y", "z"]
    csv_file = make_csv(tmp_path, cols)
    # default: substring matching
    event = {"csv_path": csv_file, "search": "y"}
    resp = lambda_handler(event, None)
    assert resp["columns"] == ["x", "\x1b[31my\x1b[0m", "z"]
    assert resp["matches"] == ["y"]


def test_lambda_handler_exact_match(tmp_path):
    cols = ["id", "customer_id"]
    csv_file = make_csv(tmp_path, cols)
    # exact_match=True should only match exact "id"
    event = {"csv_path": csv_file, "search": "id", "exact_match": True}
    resp = lambda_handler(event, None)
    assert resp["columns"] == ["\x1b[31mid\x1b[0m", "customer_id"]
    assert resp["matches"] == ["id"]


def test_lambda_handler_no_search(tmp_path):
    cols = ["a", "b"]
    csv_file = make_csv(tmp_path, cols)
    event = {"csv_path": csv_file}
    resp = lambda_handler(event, None)
    assert resp["columns"] == cols
    assert resp["matches"] == []


def test_lambda_handler_with_nrows(tmp_path):
    cols = ["x", "y", "z"]
    # create a CSV with 100 rows
    rows = [{"x": str(i), "y": str(i * 2), "z": str(i * 3)} for i in range(100)]
    data = {col: [] for col in cols}
    for row in rows:
        for col in cols:
            data[col].append(row[col])
    df = pd.DataFrame(data)
    path = tmp_path / "test_nrows.csv"
    df.to_csv(path, index=False)
    
    # use nrows to limit to 10 rows (but columns should still be all 3)
    event = {"csv_path": str(path), "nrows": 10}
    resp = lambda_handler(event, None)
    assert resp["columns"] == ["x", "y", "z"]
    assert resp["matches"] == []
