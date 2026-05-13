"""
Unit tests for the three pure helper functions added to app.py in this PR:
  - divide(a, b)
  - get_user(users, index)
  - login(user)

These functions are defined at the very top of app.py (lines 2-10), before
any Flask imports or route definitions.  The Flask route `def login():` at
line 127 would shadow the helper if we did a plain `import app`, so instead
we exec only the relevant lines directly into a fresh namespace.
"""

import os
import unittest

# ---------------------------------------------------------------------------
# Extract the three helper functions by exec-ing only their definitions.
# This avoids all Flask / DB import side-effects and the shadowing of
# `login(user)` by the `/login` route defined later in the file.
# ---------------------------------------------------------------------------
_APP_PATH = os.path.join(os.path.dirname(__file__), "app.py")

with open(_APP_PATH) as _fh:
    _lines = _fh.readlines()

# Collect lines that belong to the three helper function blocks.
# They start at line 2 (index 1) and end just before the first `import`
# statement that follows them.
_func_lines = []
for _line in _lines:
    if _line.startswith("import ") or _line.startswith("from "):
        break
    _func_lines.append(_line)

_func_src = "".join(_func_lines)

_ns: dict = {}
exec(compile(_func_src, _APP_PATH, "exec"), _ns)  # noqa: S102

divide = _ns["divide"]
get_user = _ns["get_user"]
login = _ns["login"]


# ===========================================================================
# Tests for divide(a, b)
# ===========================================================================

class TestDivide(unittest.TestCase):

    # --- happy-path cases ---

    def test_integer_division(self):
        """Dividing two integers produces the correct float result."""
        self.assertEqual(divide(10, 2), 5.0)

    def test_float_result(self):
        """Division that yields a non-integer float is returned correctly."""
        self.assertAlmostEqual(divide(7, 2), 3.5)

    def test_negative_dividend(self):
        """Negative dividend produces a negative result."""
        self.assertEqual(divide(-10, 2), -5.0)

    def test_negative_divisor(self):
        """Negative divisor produces a negative result."""
        self.assertEqual(divide(10, -2), -5.0)

    def test_both_negative(self):
        """Both arguments negative produces a positive result."""
        self.assertEqual(divide(-6, -3), 2.0)

    def test_zero_numerator(self):
        """Zero divided by any non-zero number is zero."""
        self.assertEqual(divide(0, 5), 0.0)

    def test_float_arguments(self):
        """Float arguments work correctly."""
        self.assertAlmostEqual(divide(1.0, 4.0), 0.25)

    def test_large_numbers(self):
        """Large numbers do not cause overflow."""
        self.assertAlmostEqual(divide(1e15, 1e5), 1e10)

    def test_small_fraction(self):
        """Division producing a very small number is handled correctly."""
        self.assertAlmostEqual(divide(1, 1_000_000), 1e-6)

    # --- edge / error cases ---

    def test_division_by_zero_raises(self):
        """Division by zero raises ZeroDivisionError (no guard in implementation)."""
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)

    def test_division_by_zero_with_negative_numerator_raises(self):
        """Negative numerator divided by zero still raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            divide(-99, 0)

    def test_returns_float_not_int(self):
        """Even 'clean' integer division returns a float in Python 3."""
        result = divide(6, 3)
        self.assertIsInstance(result, float)


# ===========================================================================
# Tests for get_user(users, index)
# ===========================================================================

class TestGetUser(unittest.TestCase):

    # --- list-based cases ---

    def test_first_element(self):
        """Index 0 returns the first element of a list."""
        self.assertEqual(get_user(["alice", "bob", "carol"], 0), "alice")

    def test_last_element_by_position(self):
        """Explicit last index returns the last element."""
        users = ["alice", "bob", "carol"]
        self.assertEqual(get_user(users, 2), "carol")

    def test_middle_element(self):
        """A middle index returns the correct element."""
        users = ["x", "y", "z"]
        self.assertEqual(get_user(users, 1), "y")

    def test_negative_index(self):
        """Python supports negative indexing; -1 returns the last element."""
        users = ["alice", "bob", "carol"]
        self.assertEqual(get_user(users, -1), "carol")

    def test_negative_index_second_from_last(self):
        """Negative index -2 returns the second-to-last element."""
        users = ["alice", "bob", "carol"]
        self.assertEqual(get_user(users, -2), "bob")

    def test_single_element_list(self):
        """A single-element list returns that element at index 0."""
        self.assertEqual(get_user(["only"], 0), "only")

    def test_element_is_dict(self):
        """Elements can be complex objects (dicts)."""
        users = [{"id": 1, "name": "alice"}, {"id": 2, "name": "bob"}]
        self.assertEqual(get_user(users, 1), {"id": 2, "name": "bob"})

    # --- dict-based cases ---

    def test_dict_string_key(self):
        """Works as a generic subscript; supports dict lookup by string key."""
        users = {"admin": {"role": "admin"}, "guest": {"role": "guest"}}
        self.assertEqual(get_user(users, "admin"), {"role": "admin"})

    # --- error / edge cases ---

    def test_index_out_of_range_raises(self):
        """An index beyond the list length raises IndexError (no guard)."""
        with self.assertRaises(IndexError):
            get_user(["alice", "bob"], 5)

    def test_empty_list_raises(self):
        """Accessing any index on an empty list raises IndexError."""
        with self.assertRaises(IndexError):
            get_user([], 0)

    def test_dict_missing_key_raises(self):
        """A missing dict key raises KeyError (mirrors IndexError intent)."""
        with self.assertRaises(KeyError):
            get_user({"alice": 1}, "bob")


# ===========================================================================
# Tests for login(user)
# ===========================================================================

class TestLogin(unittest.TestCase):

    # --- access-granted cases ---

    def test_admin_user_granted(self):
        """is_admin=True returns 'Access granted'."""
        result = login({"is_admin": True})
        self.assertEqual(result, "Access granted")

    def test_admin_with_extra_fields(self):
        """Extra fields in the dict do not affect the result."""
        result = login({"is_admin": True, "username": "root", "email": "r@example.com"})
        self.assertEqual(result, "Access granted")

    def test_is_admin_integer_one(self):
        """In Python, 1 == True evaluates to True, so is_admin=1 grants access."""
        result = login({"is_admin": 1})
        self.assertEqual(result, "Access granted")

    # --- access-denied / implicit-None cases ---

    def test_non_admin_returns_none(self):
        """is_admin=False causes the function to fall through and return None."""
        result = login({"is_admin": False})
        self.assertIsNone(result)

    def test_is_admin_zero_returns_none(self):
        """is_admin=0 is not equal to True, so returns None."""
        result = login({"is_admin": 0})
        self.assertIsNone(result)

    def test_is_admin_string_true_returns_none(self):
        """is_admin='True' (string) does NOT equal the boolean True; returns None."""
        result = login({"is_admin": "True"})
        self.assertIsNone(result)

    def test_is_admin_none_returns_none(self):
        """is_admin=None is not equal to True; returns None."""
        result = login({"is_admin": None})
        self.assertIsNone(result)

    def test_is_admin_empty_string_returns_none(self):
        """is_admin='' is falsy and not equal to True; returns None."""
        result = login({"is_admin": ""})
        self.assertIsNone(result)

    def test_return_value_is_exact_string(self):
        """The granted message must be exactly 'Access granted' (case-sensitive)."""
        result = login({"is_admin": True})
        self.assertEqual(result, "Access granted")
        self.assertNotEqual(result, "access granted")

    # --- error / edge cases ---

    def test_missing_is_admin_key_raises(self):
        """A dict without the 'is_admin' key raises KeyError (no guard)."""
        with self.assertRaises(KeyError):
            login({"username": "alice"})

    def test_empty_dict_raises(self):
        """An empty dict raises KeyError when 'is_admin' is accessed."""
        with self.assertRaises(KeyError):
            login({})


if __name__ == "__main__":
    unittest.main()
