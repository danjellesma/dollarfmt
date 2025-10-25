"""dollarfmt - U.S. Dollar Currency Formatting Library

A focused, dependency-light Python library for U.S. dollar currency formatting.
Provides standard formatting ($1,234.56), compact notation ($1.2K, $3.4M, $2.1B),
and Excel/PowerPoint-compatible format strings.

Main Functions:
    fmt: Standard dollar formatting with commas
    fmt_short: Compact notation with automatic K/M/B/T units
    auto_unit: Determine appropriate unit and scaled value
    excel_fmt: Generate Excel format strings for standard notation
    excel_fmt_short: Generate Excel format strings for compact notation

Example:
    >>> import dollarfmt
    >>> dollarfmt.fmt(1234.56)
    '$1,234.56'
    >>> dollarfmt.fmt_short(3_400_000)
    '$3.4M'
    >>> dollarfmt.excel_fmt()
    '"$"#,##0.00'
"""

from dollarfmt.core import fmt, fmt_short, auto_unit
from dollarfmt.excel import excel_fmt, excel_fmt_short

__version__ = "0.1.0"
__all__ = [
    "fmt",
    "fmt_short",
    "auto_unit",
    "excel_fmt",
    "excel_fmt_short",
]