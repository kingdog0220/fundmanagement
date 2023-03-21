import unittest

from fund.morningstar import MorningStar


class TestWebScraping(unittest.TestCase):
    def test_convert_to_billion_exception(self):
        morningstar = MorningStar()
        with self.assertRaises(ValueError):
            morningstar.convert_to_billion("abc")

    def test_convert_to_billion(self):
        morningstar = MorningStar()
        value = morningstar.convert_to_billion("914,754百万円")
        self.assertEquals(value, 91.48)
