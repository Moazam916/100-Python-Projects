import pandas as pd
import os
import sys
import logging
import json
from typing import Any, Dict


def get_columns_from_csv(path: str, nrows: int | None = None) -> list[str]:
    """Read a CSV file and return a list of its column names.

    Parameters
    ----------
    path : str
        Path to the CSV file. Can be local filesystem or S3 URI if pandas
        supports it.
    nrows : int | None
        Maximum number of rows to read. If ``None``, all rows are read.
        Useful for large files when you only care about column names.

    Returns
    -------
    list[str]
        Columns present in the file.
    """
    df = pd.read_csv(path, nrows=nrows)
    return list(df.columns)


def highlight_columns(columns: list[str], query: str | None, exact: bool = False) -> tuple[list[str], list[str]]:
    """Return columns with optional ANSI‑colored highlights and a list of matches.

    Parameters
    ----------
    columns : list[str]
        All column names.
    query : str | None
        Term to search for. If ``None`` the original list is returned with no
        highlights.
    exact : bool
        If ``True``, only exact (case‑insensitive) column name matches are
        highlighted. If ``False`` (default), substring matches are used.

    Returns
    -------
    tuple[list[str], list[str]]
        A tuple containing the (possibly highlighted) full list and the list
        of matching column names.

    The highlight is produced with the ANSI escape sequence for red text
    (``\x1b[31m``) and reset (``\x1b[0m``) so it will show in terminals that
    support ANSI colors.
    """
    if not query:
        return columns, []

    query_l = query.lower()
    highlighted: list[str] = []
    matches: list[str] = []

    if exact:
        # only exact matches
        for col in columns:
            if col.lower() == query_l:
                highlighted.append(f"\x1b[31m{col}\x1b[0m")
                matches.append(col)
            else:
                highlighted.append(col)
    else:
        # substring matching
        for col in columns:
            if query_l in col.lower():
                colored = f"\x1b[31m{col}\x1b[0m"
                highlighted.append(colored)
                matches.append(col)
            else:
                highlighted.append(col)
    return highlighted, matches


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda handler expecting JSON input.

    The `event` should contain a `csv_path` key with the path or URI of the
    file and an optional `search` key for the column substring to highlight.
    Optionally, pass `exact_match` (boolean) to enforce exact matching only,
    and `nrows` (int) to limit rows read (useful for large files).

    Example event::

        {
            "csv_path": "/tmp/data.csv",
            "search": "customer",
            "exact_match": false,
            "nrows": 100
        }

    If `exact_match` is ``True``, only columns that exactly match the search
    term (case‑insensitive) are highlighted. If ``False`` or omitted,
    substring matches are highlighted.

    If `nrows` is provided, only that many rows are loaded from the CSV,
    which speeds up processing of large files (columns are determined from
    the header regardless).

    Returns a JSON-serializable dictionary with the column list and matches.
    """
    csv_path = event.get("csv_path")
    if not csv_path:
        return {"error": "`csv_path` missing from event"}

    search = event.get("search")
    exact_match = event.get("exact_match", False)
    nrows = event.get("nrows")

    try:
        cols = get_columns_from_csv(csv_path, nrows=nrows)
    except Exception as e:
        logging.exception("failed to read csv")
        return {"error": str(e)}

    if search:
        highlighted, matches = highlight_columns(cols, search, exact=exact_match)
    else:
        highlighted, matches = cols, []

    return {
        "columns": highlighted,
        "matches": matches,
    }


# keep a simple entry point for local testing
if __name__ == "__main__":
    # allow quick manual invocation using a JSON string on stdin
    data = json.load(sys.stdin)
    result = lambda_handler(data, None)
    print(json.dumps(result, indent=2))