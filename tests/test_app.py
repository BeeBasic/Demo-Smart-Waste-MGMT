"""
Automated pytest test suite for Smart Waste Management business logic.

~30 % of tests are INTENTIONALLY FAILING to demonstrate:
  - missing validation
  - unsafe assumptions
  - edge cases
  - runtime risks

Failing tests are clearly marked with:
    # ❌ INTENTIONALLY FAILING TEST
"""

import sys
import types
import textwrap
import pytest

# ---------------------------------------------------------------------------
# We only need the pure-Python business-logic functions that sit at the TOP of
# app.py (before Flask / DB imports).  Loading the full module would require
# Flask-SQLAlchemy & other heavy dependencies that are irrelevant to these
# unit tests.  The helper below extracts just that code block and compiles it
# into a lightweight module object.
# ---------------------------------------------------------------------------

def _load_business_logic():
    """Return a module object containing only the business-logic functions."""
    import pathlib, ast

    app_path = pathlib.Path(__file__).resolve().parent.parent / "app.py"
    source = app_path.read_text(encoding="utf-8")

    # Parse the AST and collect every top-level FunctionDef that appears
    # BEFORE the first import / from-import statement.
    tree = ast.parse(source)
    last_func_end = 0
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            break
        if isinstance(node, ast.FunctionDef):
            last_func_end = node.end_lineno

    # Extract source lines up to (and including) the last function
    lines = source.splitlines(keepends=True)
    fragment = "".join(lines[:last_func_end])

    mod = types.ModuleType("app_logic")
    exec(compile(fragment, str(app_path), "exec"), mod.__dict__)
    return mod


_app = _load_business_logic()

divide                    = _app.divide
get_user                  = _app.get_user
login                     = _app.login
calculate_recycling_rate  = _app.calculate_recycling_rate
get_bin_status            = _app.get_bin_status
get_top_waste_categories  = _app.get_top_waste_categories
parse_sensor_reading      = _app.parse_sensor_reading
schedule_pickup           = _app.schedule_pickup
calculate_carbon_offset   = _app.calculate_carbon_offset


# =============================================================
# 1. divide()
# =============================================================

class TestDivide:
    """Tests for the divide() utility."""

    def test_divide_basic(self):
        """Standard division should return the correct result."""
        assert divide(10, 2) == 5.0

    # ❌ INTENTIONALLY FAILING TEST
    # Exposes: division by zero — no guard in divide()
    def test_divide_by_zero(self):
        """Dividing by zero should return a safe fallback, but the
        implementation has no guard and raises ZeroDivisionError."""
        result = divide(10, 0)
        assert result is None  # Expected safe behaviour


# =============================================================
# 2. get_user()
# =============================================================

class TestGetUser:
    """Tests for the get_user() utility."""

    def test_get_user_valid_index(self):
        """Accessing a valid index should return the user."""
        users = ["Alice", "Bob", "Charlie"]
        assert get_user(users, 1) == "Bob"

    # ❌ INTENTIONALLY FAILING TEST
    # Exposes: index out of range — no bounds checking in get_user()
    def test_get_user_out_of_range(self):
        """Accessing an index beyond the list should return None,
        but the implementation raises IndexError."""
        users = ["Alice", "Bob"]
        result = get_user(users, 10)
        assert result is None  # Expected safe behaviour


# =============================================================
# 3. login()
# =============================================================

class TestLogin:
    """Tests for the login() access-control helper."""

    def test_login_admin_access(self):
        """An admin user should receive 'Access granted'."""
        user = {"username": "admin", "is_admin": True}
        assert login(user) == "Access granted"

    # ❌ INTENTIONALLY FAILING TEST
    # Exposes: missing key "is_admin" → KeyError (unsafe dict access)
    def test_login_missing_admin_key(self):
        """A user dict without 'is_admin' should return 'Access denied',
        but the implementation raises KeyError."""
        user = {"username": "guest"}
        result = login(user)
        assert result == "Access denied"  # Expected safe behaviour


# =============================================================
# 4. calculate_recycling_rate()
# =============================================================

class TestCalculateRecyclingRate:
    """Tests for recycling-rate calculation."""

    def test_recycling_rate_normal(self):
        """50 recycled out of 200 total → 25 %."""
        assert calculate_recycling_rate(50, 200) == 25.0

    # ❌ INTENTIONALLY FAILING TEST (XFAIL disabled — left as a hard failure)
    # Exposes: ZeroDivisionError when no waste has been collected
    def test_recycling_rate_zero_total(self):
        """Zero total tons should return 0.0, but raises ZeroDivisionError."""
        result = calculate_recycling_rate(0, 0)
        assert result == 0.0  # Expected safe behaviour


# =============================================================
# 5. get_bin_status()
# =============================================================

class TestGetBinStatus:
    """Tests for waste-bin status lookup."""

    def test_bin_status_found(self):
        """Looking up a known bin should return its fill level."""
        bins = {"BIN-001": "full", "BIN-002": "empty"}
        assert get_bin_status(bins, "BIN-001") == "full"

    def test_bin_status_missing(self):
        """Looking up a missing bin should return None (uses .get)
        — but the implementation uses direct [] access → KeyError."""
        bins = {"BIN-001": "full"}
        # This actually works because we are testing safe behaviour here;
        # the function WILL raise KeyError, which pytest catches as a failure.
        # We wrap it to prove it raises the error.
        with pytest.raises(KeyError):
            get_bin_status(bins, "BIN-999")


# =============================================================
# 6. parse_sensor_reading()
# =============================================================

class TestParseSensorReading:
    """Tests for IoT sensor data parsing."""

    def test_parse_valid_reading(self):
        """A well-formed reading should be parsed correctly."""
        result = parse_sensor_reading("BIN-001:85.5:36.2")
        assert result == {"bin_id": "BIN-001", "fill_pct": 85.5, "temperature": 36.2}

    def test_parse_empty_string(self):
        """An empty string should return None."""
        assert parse_sensor_reading("") is None

    # ❌ INTENTIONALLY FAILING TEST
    # Exposes: weak input validation — malformed input causes IndexError
    def test_parse_malformed_reading(self):
        """A malformed reading (missing fields) should return None,
        but the implementation raises IndexError."""
        result = parse_sensor_reading("BIN-001")
        assert result is None  # Expected safe behaviour


# =============================================================
# 7. calculate_carbon_offset()
# =============================================================

class TestCalculateCarbonOffset:
    """Tests for carbon-offset estimation."""

    def test_carbon_offset_positive(self):
        """100 kg recyclable + 50 kg compostable → 285 kg CO₂ saved."""
        result = calculate_carbon_offset(100, 50)
        assert result == pytest.approx(285.0)

    def test_carbon_offset_zero(self):
        """Zero inputs should produce zero offset."""
        assert calculate_carbon_offset(0, 0) == 0.0
