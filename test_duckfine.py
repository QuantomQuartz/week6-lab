import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_initial_state(self):
        fine = DuckFine("member-42")
        self.assertEqual(fine.member_id, "member-42")
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_returns_zero_for_days_within_grace_period(self):
        fine = DuckFine("member-42")
        result = fine.charge(2)
        self.assertEqual(result, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_charge_applies_daily_fee_after_grace_days(self):
        fine = DuckFine("member-42")
        result = fine.charge(5)
        self.assertEqual(result, 1.5)
        self.assertEqual(fine.total_owed, 1.5)

    def test_charge_caps_total_fee_at_max_fee(self):
        fine = DuckFine("member-42")
        result = fine.charge(20)
        self.assertEqual(result, 5.0)
        self.assertEqual(fine.total_owed, 5.0)

    def test_charge_doubles_fee_when_deluxe(self):
        fine = DuckFine("member-42")
        result = fine.charge(5, deluxe=True)
        self.assertEqual(result, 3.0)
        self.assertEqual(fine.total_owed, 3.0)

    def test_charge_rejects_negative_days(self):
        fine = DuckFine("member-42")
        with self.assertRaises(ValueError):
            fine.charge(-1)


if __name__ == "__main__":
    unittest.main()
