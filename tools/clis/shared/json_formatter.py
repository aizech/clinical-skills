"""JSON output formatting utilities."""

import json
import sys
from typing import Any


def format_json_output(
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
) -> str:
    """Format data as JSON string.

    Args:
        data: Data to format
        indent: JSON indentation level
        sort_keys: Whether to sort object keys

    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=indent, sort_keys=sort_keys)


def print_json(
    data: Any,
    indent: int = 2,
    sort_keys: bool = False,
    file=None,
) -> None:
    """Print data as JSON to stdout or file.

    Args:
        data: Data to print
        indent: JSON indentation level
        sort_keys: Whether to sort object keys
        file: File object to write to (defaults to sys.stdout)
    """
    if file is None:
        file = sys.stdout
    print(format_json_output(data, indent, sort_keys), file=file)


def load_json_file(file_path: str) -> Any:
    """Load JSON from file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, "r") as f:
        return json.load(f)
