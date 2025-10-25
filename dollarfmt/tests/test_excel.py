"""Comprehensive tests for dollarfmt.excel module."""

import pytest
from dollarfmt.excel import excel_fmt, excel_fmt_short


class TestExcelFmt:
    """Tests for the excel_fmt() function."""
    
    def test_default_format(self):
        """Test default Excel format (2 decimals)."""
        assert excel_fmt() == '"$"#,##0.00'
    
    def test_zero_decimals(self):
        """Test format with no decimals."""
        assert excel_fmt(decimals=0) == '"$"#,##0'
    
    def test_one_decimal(self):
        """Test format with 1 decimal."""
        assert excel_fmt(decimals=1) == '"$"#,##0.0'
    
    def test_three_decimals(self):
        """Test format with 3 decimals."""
        assert excel_fmt(decimals=3) == '"$"#,##0.000'
    
    def test_many_decimals(self):
        """Test format with many decimals."""
        assert excel_fmt(decimals=5) == '"$"#,##0.00000'


class TestExcelFmtShort:
    """Tests for the excel_fmt_short() function."""
    
    def test_thousands_format(self):
        """Test K (thousands) format."""
        result = excel_fmt_short(decimals=1, unit="K")
        assert result == '"$"#,##0.0,"K"'
    
    def test_millions_format(self):
        """Test M (millions) format."""
        result = excel_fmt_short(decimals=1, unit="M")
        assert result == '"$"#,##0.0,,"M"'
    
    def test_billions_format(self):
        """Test B (billions) format."""
        result = excel_fmt_short(decimals=1, unit="B")
        assert result == '"$"#,##0.0,,,"B"'
    
    def test_trillions_format(self):
        """Test T (trillions) format."""
        result = excel_fmt_short(decimals=1, unit="T")
        assert result == '"$"#,##0.0,,,,"T"'
    
    def test_zero_decimals_k(self):
        """Test K format with no decimals."""
        result = excel_fmt_short(decimals=0, unit="K")
        assert result == '"$"#,##0,"K"'
    
    def test_zero_decimals_m(self):
        """Test M format with no decimals."""
        result = excel_fmt_short(decimals=0, unit="M")
        assert result == '"$"#,##0,,"M"'
    
    def test_two_decimals_k(self):
        """Test K format with 2 decimals."""
        result = excel_fmt_short(decimals=2, unit="K")
        assert result == '"$"#,##0.00,"K"'
    
    def test_two_decimals_m(self):
        """Test M format with 2 decimals."""
        result = excel_fmt_short(decimals=2, unit="M")
        assert result == '"$"#,##0.00,,"M"'
    
    def test_auto_returns_dict(self):
        """Test that auto returns a dictionary."""
        result = excel_fmt_short(decimals=1, unit="auto")
        assert isinstance(result, dict)
        assert len(result) == 4
        assert "K" in result
        assert "M" in result
        assert "B" in result
        assert "T" in result
    
    def test_auto_dict_values(self):
        """Test the values in auto dictionary."""
        result = excel_fmt_short(decimals=1, unit="auto")
        assert result["K"] == '"$"#,##0.0,"K"'
        assert result["M"] == '"$"#,##0.0,,"M"'
        assert result["B"] == '"$"#,##0.0,,,"B"'
        assert result["T"] == '"$"#,##0.0,,,,"T"'
    
    def test_auto_dict_zero_decimals(self):
        """Test auto dictionary with zero decimals."""
        result = excel_fmt_short(decimals=0, unit="auto")
        assert result["K"] == '"$"#,##0,"K"'
        assert result["M"] == '"$"#,##0,,"M"'
        assert result["B"] == '"$"#,##0,,,"B"'
        assert result["T"] == '"$"#,##0,,,,"T"'
    
    def test_auto_dict_two_decimals(self):
        """Test auto dictionary with two decimals."""
        result = excel_fmt_short(decimals=2, unit="auto")
        assert result["K"] == '"$"#,##0.00,"K"'
        assert result["M"] == '"$"#,##0.00,,"M"'
        assert result["B"] == '"$"#,##0.00,,,"B"'
        assert result["T"] == '"$"#,##0.00,,,,"T"'
    
    def test_invalid_unit_raises_error(self):
        """Test that invalid unit raises ValueError."""
        with pytest.raises(ValueError, match="Invalid unit"):
            excel_fmt_short(decimals=1, unit="X")
        
        with pytest.raises(ValueError, match="Invalid unit"):
            excel_fmt_short(decimals=1, unit="million")
        
        with pytest.raises(ValueError, match="Invalid unit"):
            excel_fmt_short(decimals=1, unit="")
    
    def test_case_sensitive_units(self):
        """Test that units are case-sensitive."""
        # Uppercase should work
        assert excel_fmt_short(decimals=1, unit="K") == '"$"#,##0.0,"K"'
        assert excel_fmt_short(decimals=1, unit="M") == '"$"#,##0.0,,"M"'
        
        # Lowercase should fail
        with pytest.raises(ValueError):
            excel_fmt_short(decimals=1, unit="k")
        
        with pytest.raises(ValueError):
            excel_fmt_short(decimals=1, unit="m")
    
    def test_default_parameters(self):
        """Test default parameters (decimals=1, unit='auto')."""
        result = excel_fmt_short()
        assert isinstance(result, dict)
        assert result["K"] == '"$"#,##0.0,"K"'
    
    def test_comma_count_matches_unit(self):
        """Test that comma count correctly represents division."""
        # K = divide by 1,000 (one comma for division, one in #,##0)
        k_format = excel_fmt_short(decimals=1, unit="K")
        assert k_format.count(',') == 2  # 1 for division + 1 in #,##0
        
        # M = divide by 1,000,000 (two commas for division, one in #,##0)
        m_format = excel_fmt_short(decimals=1, unit="M")
        assert m_format.count(',') == 3  # 2 for division + 1 in #,##0
        
        # B = divide by 1,000,000,000 (three commas for division, one in #,##0)
        b_format = excel_fmt_short(decimals=1, unit="B")
        assert b_format.count(',') == 4  # 3 for division + 1 in #,##0
        
        # T = divide by 1,000,000,000,000 (four commas for division, one in #,##0)
        t_format = excel_fmt_short(decimals=1, unit="T")
        assert t_format.count(',') == 5  # 4 for division + 1 in #,##0


class TestExcelIntegration:
    """Integration tests for Excel format generation."""
    
    def test_standard_and_short_consistency(self):
        """Test that standard and short formats are consistent."""
        # Both should use the same decimal format structure
        std = excel_fmt(decimals=2)
        short_k = excel_fmt_short(decimals=2, unit="K")
        
        # Standard format base
        assert '"$"#,##0.00' in std
        # Short format should have same base plus comma and unit
        assert '"$"#,##0.00' in short_k
    
    def test_all_units_have_correct_structure(self):
        """Test that all units follow the correct format structure."""
        formats = excel_fmt_short(decimals=1, unit="auto")
        
        for unit, fmt_str in formats.items():
            # All should start with "$"
            assert fmt_str.startswith('"$"')
            # All should contain #,##0
            assert '#,##0' in fmt_str
            # All should end with the unit in quotes
            assert fmt_str.endswith(f'"{unit}"')
            # All should have .1 for one decimal
            assert '.0' in fmt_str