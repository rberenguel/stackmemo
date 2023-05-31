import unittest
from colorify import colorify


class TestSuperMemo2Basics(unittest.TestCase):
    def test_basic_underscore(self):
        fied = colorify("_a_")
        self.assertEqual(fied, "#003399 a# ")

    def test_complex_underscore(self):
        fied = colorify("a_b")
        self.assertEqual(fied, "a_b")

    def test_mix(self):
        fied = colorify("`a_b`")
        self.assertEqual(fied, "#993300 a_b# ")

    def test_nl(self):
        fied = colorify("\n`foo`")
        self.assertEqual(fied, "\n#993300 foo# ")

    def test_breakage_scenario(self):
        # If lvgl breaks text, it removes styling, so…
        fied = colorify("\n`foo bar baz`")
        self.assertEqual(fied, "\n#993300 foo# #993300 bar# #993300 baz# ")


if __name__ == "__main__":
    unittest.main()
