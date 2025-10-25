"""Utility functions for the dollarfmt package.

This module provides helper functions and constants used throughout the package.
"""

from decimal import Decimal
from typing import Union

# Type alias for numeric inputs
NumericType = Union[float, int, Decimal]

# Unit thresholds
TRILLION = Decimal('1000000000000')
BILLION = Decimal('1000000000')
MILLION = Decimal('1000000')
THOUSAND = Decimal('1000')


def to_decimal(value: NumericType) -> Decimal:
    """Convert a numeric value to Decimal for precise calculations.
    
    Args:
        value: A float, int, or Decimal value
        
    Returns:
        Decimal representation of the value
        
    Examples:
        >>> to_decimal(1234.56)
        Decimal('1234.56')
        >>> to_decimal(1000)
        Decimal('1000')
    """
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def strip_zeros(formatted: str) -> str:
    """Remove trailing zeros from a formatted decimal string.
    
    Args:
        formatted: A string with decimal notation
        
    Returns:
        String with trailing zeros removed
        
    Examples:
        >>> strip_zeros("1.20")
        '1.2'
        >>> strip_zeros("1.00")
        '1'
        >>> strip_zeros("1234")
        '1234'
    """
    if '.' not in formatted:
        return formatted
    return formatted.rstrip('0').rstrip('.')