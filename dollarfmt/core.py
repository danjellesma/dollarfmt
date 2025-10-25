"""Core dollar formatting functions for the dollarfmt package.

This module provides the main formatting functions for U.S. dollar amounts,
including standard formatting and compact notation with automatic unit scaling.
"""

from decimal import Decimal, ROUND_HALF_EVEN
from typing import Tuple


def fmt(amount: float | int | Decimal, decimals: int = 2, strip_trailing_zeros: bool = False) -> str:
    """Format a dollar amount with standard notation.
    
    Args:
        amount: The dollar amount to format
        decimals: Number of decimal places (default: 2)
        strip_trailing_zeros: If True, remove trailing zeros after decimal point
        
    Returns:
        Formatted string like "$1,234.56" or "-$1,234.56" for negative values
        
    Examples:
        >>> fmt(1234.56)
        '$1,234.56'
        >>> fmt(-1234.56)
        '-$1,234.56'
        >>> fmt(1000.00, strip_trailing_zeros=True)
        '$1,000'
        >>> fmt(1234.567, decimals=3)
        '$1,234.567'
    """
    # Convert to Decimal for precision
    dec_amount = Decimal(str(amount))
    
    # Handle negative values
    is_negative = dec_amount < 0
    dec_amount = abs(dec_amount)
    
    # Round using banker's rounding (ROUND_HALF_EVEN)
    quantizer = Decimal('0.1') ** decimals
    rounded = dec_amount.quantize(quantizer, rounding=ROUND_HALF_EVEN)
    
    # Format with commas
    formatted = f"{rounded:,.{decimals}f}"
    
    # Strip trailing zeros if requested
    if strip_trailing_zeros and '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    
    # Add dollar sign and handle negative
    if is_negative:
        return f"-${formatted}"
    return f"${formatted}"


def auto_unit(amount: float | int | Decimal) -> Tuple[Decimal, str]:
    """Determine the appropriate unit and scaled value for compact formatting.
    
    Automatically scales up to the next unit when the scaled value would be >= 1000
    (requiring a comma in display). This ensures cleaner, more readable formatting.
    
    Args:
        amount: The dollar amount to analyze
        
    Returns:
        Tuple of (scaled_value, unit) where unit is "", "K", "M", "B", or "T"
        
    Examples:
        >>> auto_unit(950)
        (Decimal('950'), '')
        >>> auto_unit(1200)
        (Decimal('1.2'), 'K')
        >>> auto_unit(999_999)
        (Decimal('999.999'), 'K')
        >>> auto_unit(1_000_000)
        (Decimal('1.0'), 'M')
        >>> auto_unit(1_234_000)
        (Decimal('1.234'), 'M')
        >>> auto_unit(3_400_000)
        (Decimal('3.4'), 'M')
        >>> auto_unit(2_100_000_000)
        (Decimal('2.1'), 'B')
        >>> auto_unit(1_000_000_000_000)
        (Decimal('1.0'), 'T')
    """
    # Convert to Decimal and get absolute value for comparison
    dec_amount = Decimal(str(amount))
    abs_amount = abs(dec_amount)
    
    # Determine unit and divisor, ensuring scaled value < 1000
    # This prevents values like $1,000K and instead displays them as $1M
    # Key insight: threshold is 1000 * divisor (where scaled value would be >= 1000)
    if abs_amount < Decimal('1000'):  # < $1,000
        return dec_amount, ''
    elif abs_amount < Decimal('1000') * Decimal('1000'):  # < $1,000K (i.e., < $1,000,000)
        divisor = Decimal('1000')
        unit = 'K'
    elif abs_amount < Decimal('1000') * Decimal('1000000'):  # < $1,000M (i.e., < $1,000,000,000)
        divisor = Decimal('1000000')
        unit = 'M'
    elif abs_amount < Decimal('1000') * Decimal('1000000000'):  # < $1,000B (i.e., < $1,000,000,000,000)
        divisor = Decimal('1000000000')
        unit = 'B'
    else:  # >= $1,000B (i.e., >= $1,000,000,000,000)
        divisor = Decimal('1000000000000')
        unit = 'T'
    
    # Scale the value (preserve sign)
    scaled = dec_amount / divisor
    return scaled, unit


def fmt_short(amount: float | int | Decimal, decimals: int = 1, strip_trailing_zeros: bool = True) -> str:
    """Format a dollar amount with compact notation using K/M/B/T units.
    
    Automatically chooses the appropriate unit based on magnitude:
    - < 1,000: $950
    - < 1,000,000: $1.2K
    - < 1,000,000,000: $3.4M
    - < 1,000,000,000,000: $2.1B
    - >= 1,000,000,000,000: $1.0T
    
    Args:
        amount: The dollar amount to format
        decimals: Number of decimal places for scaled values (default: 1)
        strip_trailing_zeros: If True, remove trailing zeros after decimal point
        
    Returns:
        Formatted string with compact notation like "$1.2K" or "-$3.4M"
        
    Examples:
        >>> fmt_short(950)
        '$950'
        >>> fmt_short(1200)
        '$1.2K'
        >>> fmt_short(1000, strip_trailing_zeros=False)
        '$1.0K'
        >>> fmt_short(-3_400_000)
        '-$3.4M'
        >>> fmt_short(2_100_000_000)
        '$2.1B'
    """
    # Get scaled value and unit
    scaled_value, unit = auto_unit(amount)
    
    # Handle negative values
    is_negative = scaled_value < 0
    scaled_value = abs(scaled_value)
    
    # For values < 1000, use standard formatting without decimals
    if not unit:
        # Round to integer using banker's rounding
        rounded = scaled_value.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
        formatted = f"{rounded:,.0f}"
    else:
        # Round using banker's rounding
        quantizer = Decimal('0.1') ** decimals
        rounded = scaled_value.quantize(quantizer, rounding=ROUND_HALF_EVEN)
        
        # Format with specified decimals
        formatted = f"{rounded:.{decimals}f}"
        
        # Strip trailing zeros if requested
        if strip_trailing_zeros and '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
    
    # Build final string
    result = f"${formatted}{unit}"
    if is_negative:
        result = f"-{result}"
    
    return result