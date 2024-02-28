from django.test import SimpleTestCase
from app import calc

class CalcTest(SimpleTestCase):
    def test_add_numbers(self):
        r = calc.add(3, 5)
        self.assertEqual(r,8)

    def test_subtract_numbers(self):
        r = calc.subtract(5,3)
        self.assertEqual(r,2)