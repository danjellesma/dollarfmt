"""Comprehensive tests for dollarfmt.core module."""

import pytest
from decimal import Decimal
from dollarfmt.core import fmt, fmt_short, auto_unit


class TestFmt:
    """Tests for the fmt() function."""
    
    def test_basic_formatting(self):
        """Test basic dollar formatting."""
        assert fmt(1234.56) == "$1,234.56"
        assert fmt(1000) == "$1,000.00"
        assert fmt(0) == "$0.00"
    
    def test_negative_values(self):
        """Test negative value formatting."""
        assert fmt(-1234.56) == "-$1,234.56"
        assert fmt(-1000) == "-$1,000.00"
        assert fmt(-0.01) == "-$0.01"
    
    def test_large_numbers(self):
        """Test formatting of large numbers."""
        assert fmt(1_000_000) == "$1,000,000.00"
        assert fmt(1_234_567_890.12) == "$1,234,567,890.12"
    
    def test_decimal_places(self):
        """Test custom decimal places."""
        assert fmt(1234.567, decimals=0) == "$1,235"
        assert fmt(1234.567, decimals=1) == "$1,234.6"
        assert fmt(1234.567, decimals=3) == "$1,234.567"
        assert fmt(1234.567, decimals=4) == "$1,234.5670"
    
    def test_strip_trailing_zeros(self):
        """Test stripping of trailing zeros."""
        assert fmt(1000.00, strip_trailing_zeros=True) == "$1,000"
        assert fmt(1234.50, strip_trailing_zeros=True) == "$1,234.5"
        assert fmt(1234.00, strip_trailing_zeros=True) == "$1,234"
        assert fmt(1234.56, strip_trailing_zeros=True) == "$1,234.56"
    
    def test_bankers_rounding(self):
        """Test banker's rounding (round half to even)."""
        # Round half to even: .5 rounds to nearest even number
        assert fmt(1.125, decimals=2) == "$1.12"  # 1.125 -> 1.12 (even)
        assert fmt(1.135, decimals=2) == "$1.14"  # 1.135 -> 1.14 (even)
        assert fmt(2.5, decimals=0) == "$2"       # 2.5 -> 2 (even)
        assert fmt(3.5, decimals=0) == "$4"       # 3.5 -> 4 (even)
    
    def test_decimal_input(self):
        """Test with Decimal input."""
        assert fmt(Decimal("1234.56")) == "$1,234.56"
        assert fmt(Decimal("-1234.56")) == "-$1,234.56"
    
    def test_integer_input(self):
        """Test with integer input."""
        assert fmt(1234) == "$1,234.00"
        assert fmt(-1234) == "-$1,234.00"
    
    def test_small_values(self):
        """Test very small values."""
        assert fmt(0.01) == "$0.01"
        assert fmt(0.001, decimals=3) == "$0.001"
        assert fmt(0.0001, decimals=4) == "$0.0001"


class TestAutoUnit:
    """Tests for the auto_unit() function."""
    
    def test_no_unit(self):
        """Test values that don't need a unit (< 1000)."""
        value, unit = auto_unit(0)
        assert value == Decimal('0')
        assert unit == ''
        
        value, unit = auto_unit(999)
        assert value == Decimal('999')
        assert unit == ''
        
        value, unit = auto_unit(500.5)
        assert value == Decimal('500.5')
        assert unit == ''
    
    def test_thousands(self):
        """Test thousand unit (K)."""
        value, unit = auto_unit(1000)
        assert value == Decimal('1')
        assert unit == 'K'
        
        value, unit = auto_unit(1200)
        assert value == Decimal('1.2')
        assert unit == 'K'
        
        # Values up to 999,999 stay in K (may round to display as 1000K)
        value, unit = auto_unit(999_999)
        assert value == Decimal('999.999')
        assert unit == 'K'
        
        # Values >= 1,000,000 scale to M to avoid displaying commas
        value, unit = auto_unit(1_000_000)
        assert value == Decimal('1')
        assert unit == 'M'
        
        value, unit = auto_unit(1_234_000)
        assert value == Decimal('1.234')
        assert unit == 'M'
    
    def test_millions(self):
        """Test million unit (M)."""
        value, unit = auto_unit(1_000_000)
        assert value == Decimal('1')
        assert unit == 'M'
        
        value, unit = auto_unit(3_400_000)
        assert value == Decimal('3.4')
        assert unit == 'M'
        
        # Values up to 999,999,999 stay in M (may round to display as 1000M)
        value, unit = auto_unit(999_999_999)
        assert value == Decimal('999.999999')
        assert unit == 'M'
        
        # Values >= 1,000,000,000 scale to B to avoid displaying commas
        value, unit = auto_unit(1_000_000_000)
        assert value == Decimal('1')
        assert unit == 'B'
        
        value, unit = auto_unit(1_234_000_000)
        assert value == Decimal('1.234')
        assert unit == 'B'
    
    def test_billions(self):
        """Test billion unit (B)."""
        value, unit = auto_unit(1_000_000_000)
        assert value == Decimal('1')
        assert unit == 'B'
        
        value, unit = auto_unit(2_100_000_000)
        assert value == Decimal('2.1')
        assert unit == 'B'
        
        # Values up to 999,999,999,999 stay in B (may round to display as 1000B)
        value, unit = auto_unit(999_999_999_999)
        assert value == Decimal('999.999999999')
        assert unit == 'B'
        
        # Values >= 1,000,000,000,000 scale to T to avoid displaying commas
        value, unit = auto_unit(1_000_000_000_000)
        assert value == Decimal('1')
        assert unit == 'T'
        
        value, unit = auto_unit(1_234_000_000_000)
        assert value == Decimal('1.234')
        assert unit == 'T'
    
    def test_trillions(self):
        """Test trillion unit (T)."""
        value, unit = auto_unit(1_000_000_000_000)
        assert value == Decimal('1')
        assert unit == 'T'
        
        value, unit = auto_unit(1_500_000_000_000)
        assert value == Decimal('1.5')
        assert unit == 'T'
        
        value, unit = auto_unit(999_000_000_000_000)
        assert value == Decimal('999')
        assert unit == 'T'
    
    def test_negative_values(self):
        """Test negative values preserve sign."""
        value, unit = auto_unit(-1200)
        assert value == Decimal('-1.2')
        assert unit == 'K'
        
        value, unit = auto_unit(-3_400_000)
        assert value == Decimal('-3.4')
        assert unit == 'M'


class TestFmtShort:
    """Tests for the fmt_short() function."""
    
    def test_no_unit_values(self):
        """Test values < 1000 (no unit)."""
        assert fmt_short(0) == "$0"
        assert fmt_short(500) == "$500"
        assert fmt_short(999) == "$999"
    
    def test_thousands(self):
        """Test thousand formatting (K)."""
        assert fmt_short(1000) == "$1K"
        assert fmt_short(1200) == "$1.2K"
        assert fmt_short(1500) == "$1.5K"
        assert fmt_short(999_999) == "$1000K"
        # Values >= 1,000K scale to M
        assert fmt_short(1_234_000) == "$1.2M"
    
    def test_millions(self):
        """Test million formatting (M)."""
        assert fmt_short(1_000_000) == "$1M"
        assert fmt_short(3_400_000) == "$3.4M"
        assert fmt_short(10_500_000) == "$10.5M"
        assert fmt_short(999_999_999) == "$1000M"
        # Values >= 1,000M scale to B
        assert fmt_short(1_234_000_000) == "$1.2B"
    
    def test_billions(self):
        """Test billion formatting (B)."""
        assert fmt_short(1_000_000_000) == "$1B"
        assert fmt_short(2_100_000_000) == "$2.1B"
        assert fmt_short(50_000_000_000) == "$50B"
        assert fmt_short(999_999_999_999) == "$1000B"
        # Values >= 1,000B scale to T
        assert fmt_short(1_234_000_000_000) == "$1.2T"
    
    def test_trillions(self):
        """Test trillion formatting (T)."""
        assert fmt_short(1_000_000_000_000) == "$1T"
        assert fmt_short(1_500_000_000_000) == "$1.5T"
    
    def test_negative_values(self):
        """Test negative value formatting."""
        assert fmt_short(-1200) == "-$1.2K"
        assert fmt_short(-3_400_000) == "-$3.4M"
        assert fmt_short(-2_100_000_000) == "-$2.1B"
        assert fmt_short(-500) == "-$500"
    
    def test_custom_decimals(self):
        """Test custom decimal places."""
        assert fmt_short(1234, decimals=0) == "$1K"
        assert fmt_short(1234, decimals=2) == "$1.23K"
        assert fmt_short(1234567, decimals=0) == "$1M"
        assert fmt_short(1234567, decimals=2) == "$1.23M"
    
    def test_no_strip_trailing_zeros(self):
        """Test keeping trailing zeros."""
        assert fmt_short(1000, strip_trailing_zeros=False) == "$1.0K"
        assert fmt_short(2_000_000, strip_trailing_zeros=False) == "$2.0M"
        assert fmt_short(3_000_000_000, strip_trailing_zeros=False) == "$3.0B"
    
    def test_strip_trailing_zeros(self):
        """Test stripping trailing zeros (default behavior)."""
        assert fmt_short(1000) == "$1K"
        assert fmt_short(1100) == "$1.1K"
        assert fmt_short(2_000_000) == "$2M"
        assert fmt_short(2_500_000) == "$2.5M"
    
    def test_bankers_rounding(self):
        """Test banker's rounding in short format."""
        # 1250 / 1000 = 1.25, rounds to 1.2 (even)
        assert fmt_short(1250, decimals=1) == "$1.2K"
        # 1350 / 1000 = 1.35, rounds to 1.4 (even)
        assert fmt_short(1350, decimals=1) == "$1.4K"
    
    def test_threshold_boundaries(self):
        """Test values at unit boundaries."""
        assert fmt_short(999) == "$999"
        assert fmt_short(1000) == "$1K"
        # At boundary, stays in current unit (999.999K)
        assert fmt_short(999_999) == "$1000K"
        # Crosses 1000K threshold, scales to M
        assert fmt_short(1_000_000) == "$1M"
        assert fmt_short(1_234_000) == "$1.2M"
        # At boundary, stays in current unit (999.999999M)
        assert fmt_short(999_999_999) == "$1000M"
        # Crosses 1000M threshold, scales to B
        assert fmt_short(1_000_000_000) == "$1B"
        assert fmt_short(1_234_000_000) == "$1.2B"
    
    def test_decimal_input(self):
        """Test with Decimal input."""
        assert fmt_short(Decimal("1234")) == "$1.2K"
        assert fmt_short(Decimal("3400000")) == "$3.4M"
    
    def test_float_precision(self):
        """Test that float inputs are handled correctly."""
        assert fmt_short(1234.56) == "$1.2K"
        assert fmt_short(3_456_789.12) == "$3.5M"