import unittest
import memo



class TestSuperMemo2Basics(unittest.TestCase):
    def test_ef_13(self):
        efp = memo.ef(1, 1.5)
        self.assertEqual(efp, 1.3)
    def test_ef_inc(self):
        efp = memo.ef(4.5, 1.5)
        self.assertGreater(efp, 1.5)
    def test_low_q(self):
        i_n = memo.interval(1, 12, 12, 2.5)
        ef_p = memo.ef(1, 2.5)
        self.assertEqual(i_n, 1)
        self.assertLess(ef_p, 2.5)
        self.assertGreater(ef_p, 1.5)

if __name__ == '__main__':
    unittest.main()

