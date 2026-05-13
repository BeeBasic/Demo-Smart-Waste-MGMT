"""
Unit tests for the divide() function added in app.py.

The divide() function is defined at module level before Flask/DB imports,
so we isolate it by mocking heavy dependencies before importing the module.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch


def _import_divide():
    """Import only the divide function from app.py without triggering Flask/DB init."""
    # Stub out all problematic modules before importing app
    stubs = {
        "flask": MagicMock(),
        "werkzeug": MagicMock(),
        "werkzeug.utils": MagicMock(),
        "werkzeug.security": MagicMock(),
        "config": MagicMock(),
        "database": MagicMock(),
        "database.db": MagicMock(),
        "database.models": MagicMock(),
        "forms": MagicMock(),
        "models": MagicMock(),
        "models.classifier": MagicMock(),
    }

    # Patch sys.modules so imports inside app.py resolve to stubs
    with patch.dict(sys.modules, stubs):
        # Also patch os.makedirs to prevent filesystem side effects
        with patch("os.makedirs"):
            import importlib
            # Remove cached version if already imported
            sys.modules.pop("app", None)
            import app as _app
            divide_fn = _app.divide
    return divide_fn


# Load divide once for all tests
divide = _import_divide()


class TestDivideBasicArithmetic(unittest.TestCase):
    """Tests for standard numeric division behaviour."""

    def test_integer_division_exact(self):
        """Dividing two integers that yield an exact float result."""
        self.assertEqual(divide(10, 2), 5.0)

    def test_integer_division_fractional(self):
        """Dividing integers that yield a fractional result."""
        self.assertAlmostEqual(divide(7, 2), 3.5)

    def test_float_inputs(self):
        """Dividing two float values."""
        self.assertAlmostEqual(divide(10.0, 4.0), 2.5)

    def test_mixed_int_and_float(self):
        """Dividing an int by a float."""
        self.assertAlmostEqual(divide(9, 2.0), 4.5)

    def test_divisor_of_one(self):
        """Dividing any number by 1 should return that number."""
        self.assertEqual(divide(42, 1), 42.0)

    def test_numerator_equals_denominator(self):
        """Dividing equal numbers should return 1.0."""
        self.assertEqual(divide(7, 7), 1.0)


class TestDivideSignHandling(unittest.TestCase):
    """Tests for sign combinations in division."""

    def test_negative_numerator(self):
        """Negative numerator divided by positive denominator."""
        self.assertEqual(divide(-10, 2), -5.0)

    def test_negative_denominator(self):
        """Positive numerator divided by negative denominator."""
        self.assertEqual(divide(10, -2), -5.0)

    def test_both_negative(self):
        """Both operands negative should yield a positive result."""
        self.assertEqual(divide(-10, -2), 5.0)

    def test_negative_float_result(self):
        """Negative float result."""
        self.assertAlmostEqual(divide(-7, 2), -3.5)


class TestDivideZeroNumerator(unittest.TestCase):
    """Tests for zero as the numerator."""

    def test_zero_divided_by_positive(self):
        """Zero divided by a positive number returns zero."""
        self.assertEqual(divide(0, 5), 0.0)

    def test_zero_divided_by_negative(self):
        """Zero divided by a negative number returns zero (or -0.0 which == 0.0)."""
        self.assertEqual(divide(0, -3), 0.0)

    def test_zero_divided_by_float(self):
        """Zero divided by a float returns zero."""
        self.assertEqual(divide(0, 0.5), 0.0)


class TestDivideDivisionByZero(unittest.TestCase):
    """Tests for division-by-zero error propagation."""

    def test_integer_division_by_zero_raises(self):
        """Dividing an integer by zero should raise ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)

    def test_float_division_by_zero_raises(self):
        """Dividing a float by zero should raise ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            divide(1.0, 0)

    def test_negative_divided_by_zero_raises(self):
        """Dividing a negative number by zero should raise ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            divide(-5, 0)

    def test_zero_divided_by_zero_raises(self):
        """Zero divided by zero is indeterminate; should raise ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            divide(0, 0)


class TestDivideSpecialValues(unittest.TestCase):
    """Boundary, precision, and regression tests."""

    def test_small_fractional_result(self):
        """1 / 3 should approximate 0.3333..."""
        result = divide(1, 3)
        self.assertAlmostEqual(result, 1 / 3, places=10)

    def test_large_integers(self):
        """Large integer inputs should not overflow (Python ints are arbitrary precision)."""
        result = divide(10**18, 10**9)
        self.assertAlmostEqual(result, 10**9, places=0)

    def test_very_small_denominator(self):
        """Dividing by a very small float produces a large result."""
        result = divide(1.0, 1e-10)
        self.assertAlmostEqual(result, 1e10, places=0)

    def test_returns_float_for_int_inputs(self):
        """Python 3 true division always returns a float for int/int."""
        result = divide(4, 2)
        self.assertIsInstance(result, float)

    def test_large_float_division(self):
        """Division of large floats should not raise (no overflow to inf check)."""
        result = divide(1e200, 1e100)
        self.assertAlmostEqual(result, 1e100, delta=1e90)

    def test_regression_negative_zero(self):
        """Regression: divide(0, -1) should compare equal to 0.0 regardless of sign bit."""
        self.assertEqual(divide(0, -1), 0.0)


if __name__ == "__main__":
    unittest.main()
