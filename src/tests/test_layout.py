import utils
# pylint: disable=import-error
from cores.layout.parser import Parser
import unittest


class LayoutTest(unittest.TestCase):
    def test(self):
        p = Parser()
        self.assertTrue(p)
