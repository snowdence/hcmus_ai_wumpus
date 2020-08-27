import unittest
# pylint: disable=import-error
from cores.kb_solve.kb import KB


class KBTest(unittest.TestCase):
    kb = KB(10, 10)

    def test_get_adj_1(self):
        kb = KB(4, 4)
        x, y = 1, 1
        output_1 = kb.get_all_adj_4_direction(x,  y)
        expect_1 = [2, 5, 7, 10]
        output_1.sort()
        expect_1.sort()
        self.assertEqual(output_1, expect_1)

    def test_get_adj_2(self):
        kb = KB(4, 4)
        x, y = 1, 0
        output_2 = kb.get_all_adj_4_direction(x,  y)
        expect_2 = [1, 3, 6]
        output_2.sort()
        expect_2.sort()
        self.assertEqual(output_2, expect_2)

    def test_adj_to_xy(self):
        out1 = self.kb.adj_to_xy(11)
        out2 = self.kb.adj_to_xy(22)
        expect_1 = (0, 1)
        expect_2 = (1, 2)
        self.assertEqual(out1, expect_1)
        self.assertEqual(out2, expect_2)

    def test_xy_to_adj(self):
        out1 = self.kb.xy_to_adj(0, 1)
        out2 = self.kb.xy_to_adj(1, 2)
        expect_1 = 11
        expect_2 = 22
        self.assertEqual(out1, expect_1)
        self.assertEqual(out2, expect_2)


if __name__ == "__main__":
    unittest.main()
