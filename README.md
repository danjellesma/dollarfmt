# dollarfmt

A focused, dependency-light Python library for **U.S. dollar currency formatting**.

Provides standard formatting (`$1,234.56`), compact notation with automatic unit scaling (`$1.2K`, `$3.4M`, `$2.1B`, `$1.0T`), and generation of matching **Excel and PowerPoint-compatible format strings**.

## Features

- 🎯 **Simple & Focused**: Only USD formatting, no locale complexity
- 📊 **Excel Integration**: Generate format strings for Excel/PowerPoint
- 🔢 **Precise**: Uses `Decimal` for accurate financial calculations
- 🎨 **Flexible**: Standard and compact notation with customizable decimals
- 🚀 **Zero Dependencies**: Only uses Python standard library
- ✅ **Well Tested**: 100% test coverage

## Installation

```bash
pip install dollarfmt
```

## Quick Start

```python
import dollarfmt

# Standard formatting
dollarfmt.fmt(1234.56)           # '$1,234.56'
dollarfmt.fmt(-1234.56)          # '-$1,234.56'
dollarfmt.fmt(1000, decimals=0)  # '$1,000'

# Compact notation with automatic units
dollarfmt.fmt_short(1200)           # '$1.2K'
dollarfmt.fmt_short(3400000)       # '$3.4M'
dollarfmt.fmt_short(2100000000)   # '$2.1B'
dollarfmt.fmt_short(1500000000000)  # '$1.5T'

# Get unit and scaled value
value, unit = dollarfmt.auto_unit(3400000)  # (Decimal('3.4'), 'M')

# Excel format strings
dollarfmt.excel_fmt()                    # '"$"#,##0.00'
dollarfmt.excel_fmt_short(unit="M")      # '"$"#,##0.0,,"M"'
```

## API Reference

### Core Functions

#### `fmt(amount, decimals=2, strip_trailing_zeros=False)`

Format a dollar amount with standard notation.

**Parameters:**
- `amount` (float | int | Decimal): The dollar amount to format
- `decimals` (int): Number of decimal places (default: 2)
- `strip_trailing_zeros` (bool): Remove trailing zeros after decimal point

**Returns:** Formatted string like `$1,234.56`

**Examples:**
```python
dollarfmt.fmt(1234.56)                        # '$1,234.56'
dollarfmt.fmt(-1234.56)                       # '-$1,234.56'
dollarfmt.fmt(1000.00, strip_trailing_zeros=True)  # '$1,000'
dollarfmt.fmt(1234.567, decimals=3)           # '$1,234.567'
```

#### `fmt_short(amount, decimals=1, strip_trailing_zeros=True)`

Format a dollar amount with compact notation using K/M/B/T units.

Automatically chooses the appropriate unit based on magnitude to avoid displaying commas in the scaled value:
- `< 1,000`: `$950`
- `< 1,000,000`: `$1.2K` to `$999.9K`
- `< 1,000,000,000`: `$1M` to `$999.9M`
- `< 1,000,000,000,000`: `$1B` to `$999.9B`
- `>= 1,000,000,000,000`: `$1T+`

Values automatically scale to the next unit when they would reach 1,000 in the current unit (e.g., $1,234,000 displays as $1.2M, not $1,234K).

**Parameters:**
- `amount` (float | int | Decimal): The dollar amount to format
- `decimals` (int): Number of decimal places for scaled values (default: 1)
- `strip_trailing_zeros` (bool): Remove trailing zeros after decimal point (default: True)

**Returns:** Formatted string with compact notation

**Examples:**
```python
dollarfmt.fmt_short(950)                      # '$950'
dollarfmt.fmt_short(1200)                     # '$1.2K'
dollarfmt.fmt_short(1000, strip_trailing_zeros=False)  # '$1.0K'
dollarfmt.fmt_short(-3400000)               # '-$3.4M'
dollarfmt.fmt_short(2100000000)            # '$2.1B'
dollarfmt.fmt_short(1234000)               # '$1.2M' (not $1,234K)
```

#### `auto_unit(amount)`

Determine the appropriate unit and scaled value for compact formatting.

Values are automatically scaled to prevent comma displays (e.g., values >= 1,000,000 use 'M' instead of 'K' to avoid formats like $1,234K).

**Parameters:**
- `amount` (float | int | Decimal): The dollar amount to analyze

**Returns:** Tuple of `(scaled_value, unit)` where unit is `""`, `"K"`, `"M"`, `"B"`, or `"T"`

**Examples:**
```python
dollarfmt.auto_unit(950)           # (Decimal('950'), '')
dollarfmt.auto_unit(1200)          # (Decimal('1.2'), 'K')
dollarfmt.auto_unit(1234000)       # (Decimal('1.234'), 'M')
dollarfmt.auto_unit(3400000)       # (Decimal('3.4'), 'M')
dollarfmt.auto_unit(2100000000)    # (Decimal('2.1'), 'B')
```

### Excel Integration Functions

#### `excel_fmt(decimals=2)`

Generate an Excel format string for standard dollar notation.

**Parameters:**
- `decimals` (int): Number of decimal places (default: 2)

**Returns:** Excel format string

**Examples:**
```python
dollarfmt.excel_fmt()           # '"$"#,##0.00'
dollarfmt.excel_fmt(decimals=0) # '"$"#,##0'
dollarfmt.excel_fmt(decimals=3) # '"$"#,##0.000'
```

#### `excel_fmt_short(decimals=1, unit="auto")`

Generate Excel format strings for compact dollar notation with K/M/B/T units.

**Parameters:**
- `decimals` (int): Number of decimal places (default: 1)
- `unit` (str): Specific unit (`"K"`, `"M"`, `"B"`, `"T"`) or `"auto"` for all formats

**Returns:** 
- If `unit` is specified: Single format string
- If `unit="auto"`: Dictionary with all format strings

**Examples:**
```python
dollarfmt.excel_fmt_short(unit="K")  # '"$"#,##0.0,"K"'
dollarfmt.excel_fmt_short(unit="M")  # '"$"#,##0.0,,"M"'
dollarfmt.excel_fmt_short(unit="B")  # '"$"#,##0.0,,,"B"'

# Get all formats
formats = dollarfmt.excel_fmt_short(unit="auto")
# {
#     "K": '"$"#,##0.0,"K"',
#     "M": '"$"#,##0.0,,"M"',
#     "B": '"$"#,##0.0,,,"B"',
#     "T": '"$"#,##0.0,,,,"T"'
# }
```

## Excel Format String Reference

The table below shows how Excel format strings work. Note that in Excel, you must manually choose which format to apply - Excel does not auto-scale like Python's `fmt_short()` function.

| Unit | Divisor | Excel Format String | Example Value | Displays As |
|------|---------|---------------------|---------------|-------------|
| (none) | 1 | `"$"#,##0.00` | 1234.56 | $1,234.56 |
| K | 1,000 | `"$"#,##0.0,"K"` | 1234567 | $1,234.6K |
| M | 1,000,000 | `"$"#,##0.0,,"M"` | 1234567890 | $1,234.6M |
| B | 1,000,000,000 | `"$"#,##0.0,,,"B"` | 1234567890123 | $1,234.6B |
| T | 1,000,000,000,000 | `"$"#,##0.0,,,,"T"` | 1234567890123456 | $1,234.6T |

**Note:** In Excel format strings, each comma (`,`) after the number format divides the value by 1,000. Unlike Python's `fmt_short()` which auto-scales to avoid comma displays (e.g., $1,234K becomes $1.2M), Excel format strings require you to choose the appropriate unit for your data range.

## Using with Excel/PowerPoint

### Python-PPTX Example

```python
from pptx import Presentation
from pptx.util import Inches
import dollarfmt

# Create presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])

# Add text with formatted dollar amount
textbox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(3), Inches(1))
text_frame = textbox.text_frame
text_frame.text = f"Revenue: {dollarfmt.fmt_short(3400000)}"

prs.save('presentation.pptx')
```

### OpenPyXL Example

```python
from openpyxl import Workbook
import dollarfmt

wb = Workbook()
ws = wb.active

# Write value and apply format
ws['A1'] = 1234567
ws['A1'].number_format = dollarfmt.excel_fmt_short(unit="K")

# Value displays as: $1,234.6K
wb.save('workbook.xlsx')
```

## Technical Details

### Rounding

All functions use **banker's rounding** (round half to even) via `Decimal.quantize()` with `ROUND_HALF_EVEN`. This is the standard rounding method for financial calculations.

```python
dollarfmt.fmt(1.125, decimals=2)  # '$1.12' (rounds to even)
dollarfmt.fmt(1.135, decimals=2)  # '$1.14' (rounds to even)
```

### Precision

All calculations use Python's `Decimal` type for precise financial arithmetic, avoiding floating-point errors.

### Negative Values

Negative values are formatted with the minus sign before the dollar sign:

```python
dollarfmt.fmt(-1234.56)        # '-$1,234.56'
dollarfmt.fmt_short(-3400000) # '-$3.4M'
```

## Requirements

- Python 3.10+
- No external dependencies (uses only standard library)

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/danjellesma/dollarfmt.git
cd dollarfmt

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dollarfmt --cov-report=html

# Run specific test file
pytest dollarfmt/tests/test_core.py
```

### Code Quality

```bash
# Format code
ruff format

# Lint code
ruff check

# Type checking
mypy dollarfmt
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Dan Jellesma

## Changelog

### 0.1.1
- Fix formatting for auto function

### 0.1.0 (2025)
- Initial release
- Core formatting functions (`fmt`, `fmt_short`, `auto_unit`)
- Excel integration functions (`excel_fmt`, `excel_fmt_short`)
- Comprehensive test suite
- Full documentation
