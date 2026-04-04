"""Base CLI utilities with common argparse setup and error handling."""

import argparse
import logging
import sys
from typing import Optional


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging for CLI tools.

    Args:
        verbose: Enable DEBUG level logging
        quiet: Suppress INFO level output (only WARNING and ERROR)
    """
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_base_parser(
    description: str,
    version: Optional[str] = None,
    add_common_args: bool = True,
) -> argparse.ArgumentParser:
    """Create a base argument parser with common options.

    Args:
        description: Tool description for help text
        version: Version string for --version flag
        add_common_args: Whether to add --verbose and --quiet flags

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    if version:
        parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {version}",
        )

    if add_common_args:
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable verbose output",
        )
        parser.add_argument(
            "--quiet",
            "-q",
            action="store_true",
            help="Suppress non-error output",
        )

    return parser


def handle_error(message: str, exit_code: int = 1) -> None:
    """Handle and display errors consistently.

    Args:
        message: Error message to display
        exit_code: Exit code to use
    """
    logging.error(message)
    sys.exit(exit_code)


class CLIError(Exception):
    """Base exception for CLI errors."""

    def __init__(self, message: str, exit_code: int = 1):
        self.message = message
        self.exit_code = exit_code
        super().__init__(self.message)
