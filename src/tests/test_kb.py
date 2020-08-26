import utils
import unittest
# pylint: disable=import-error
from cores.kb_solve.kb import KB


class KBTest(unittest.TestCase):
    def test(self):
        kb = KB(10, 10)
        x, y = 1, 1
        output_1 = kb.get_all_adj_4_direction(x, 10 - y - 1)
        expect_1 = [11, 13, 22, 2]
        output_1.sort()
        expect_1.sort()
        self.assertEqual(output_1, expect_1)

    def test2(self):
        kb = KB(10, 10)
        x, y = 1, 0
        output_2 = kb.get_all_adj_4_direction(x, 10 - y - 1)
        expect_2 = [1, 12, 3]
        output_2.sort()
        expect_2.sort()
        self.assertEqual(output_2, expect_2)
