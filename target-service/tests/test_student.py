"""Student regression: discounted goods just below the free-shipping threshold."""
import unittest
from decimal import Decimal as D
from orders.pricing import quote


class StudentRegression(unittest.TestCase):
    def test_multi_quantity_line_discounted_just_below_threshold(self):
        result = quote([{"unit_price": D("37.335"), "quantity": 3}], D("0.11"))
        self.assertEqual(result["subtotal"], D("112.01"))
        self.assertEqual(result["shipping"], D("5.00"))
        self.assertEqual(result["total"], D("104.69"))


if __name__ == "__main__":
    unittest.main()
