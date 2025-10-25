"""Excel and PowerPoint format string generation for dollar amounts.

This module provides functions to generate Excel/PowerPoint-compatible number
format strings for both standard and compact dollar notation.
"""

from typing import Dict


def excel_fmt(decimals: int = 2) -> str:
    """Generate an Excel format string for standard dollar notation.
    
    Args:
        decimals: Number of decimal places (default: 2)
        
    Returns:
        Excel format string like "$#,##0.00"
        
    Examples:
        >>> excel_fmt()
        '"$"#,##0.00'
        >>> excel_fmt(decimals=0)
        '"$"#,##0'
        >>> excel_fmt(decimals=3)
        '"$"#,##0.000'
    """
    if decimals == 0:
        return '"$"#,##0'
    
    # Build decimal portion
    decimal_part = '0' * decimals
    return f'"$"#,##0.{decimal_part}'


def excel_fmt_short(decimals: int = 1, unit: str = "auto") -> str | Dict[str, str]:
    """Generate Excel format strings for compact dollar notation with K/M/B/T units.
    
    Args:
        decimals: Number of decimal places (default: 1)
        unit: Specific unit ("K", "M", "B", "T") or "auto" for all formats
        
    Returns:
        If unit is specified: Single format string like "$#,##0.0,\"K\""
        If unit is "auto": Dictionary with all format strings
        
    Examples:
        >>> excel_fmt_short(decimals=1, unit="K")
        '"$"#,##0.0,"K"'
        >>> excel_fmt_short(decimals=1, unit="M")
        '"$"#,##0.0,,"M"'
        >>> excel_fmt_short(decimals=0, unit="B")
        '"$"#,##0,,,"B"'
        >>> result = excel_fmt_short(decimals=1, unit="auto")
        >>> result["K"]
        '"$"#,##0.0,"K"'
    """
    # Build the base format with decimals
    if decimals == 0:
        base = '"$"#,##0'
    else:
        decimal_part = '0' * decimals
        base = f'"$"#,##0.{decimal_part}'
    
    # Define format strings for each unit
    # Each comma in Excel divides by 1,000
    formats = {
        'K': f'{base},"K"',      # One comma = divide by 1,000
        'M': f'{base},,"M"',     # Two commas = divide by 1,000,000
        'B': f'{base},,,"B"',    # Three commas = divide by 1,000,000,000
        'T': f'{base},,,,"T"',   # Four commas = divide by 1,000,000,000,000
    }
    
    # Return specific format or all formats
    if unit == "auto":
        return formats
    elif unit in formats:
        return formats[unit]
    else:
        raise ValueError(f"Invalid unit: {unit}. Must be 'K', 'M', 'B', 'T', or 'auto'")