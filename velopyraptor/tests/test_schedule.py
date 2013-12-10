import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schedule import Schedule


class TestSchedule(unittest.TestCase):

    def test_init(self):
        """
        Tests the values of pieces of the schedule upon init
        """
        t = 10
        test_range = range(t)
        s = Schedule(t, t)

        #s.c and s.d are range sequences initially
        for i in test_range:
            self.assertTrue(i == s.c[i])
            self.assertTrue(i == s.d[i])

        # Assert that the length of the xors list is 0
        self.assertTrue(0 == len(s.xors))

    def test_exhange_row(self):
        """Tests the exchanging of rows in the schedule"""
        t = 10
        s = Schedule(t, t)
        self.assertTrue(s.d[0] == 0)
        self.assertTrue(s.d[1] == 1)
        # Swap rows 0 and 1
        s.exchange_row(0, 1)
        self.assertTrue(s.d[0] == 1)
        self.assertTrue(s.d[1] == 0)

    def test_exchange_column(self):
        """Tests the exchanging of columns in the schedule"""
        t = 10
        s = Schedule(t, t)
        self.assertTrue(s.c[0] == 0)
        self.assertTrue(s.c[1] == 1)
        s.exchange_column(0, 1)
        self.assertTrue(s.c[0] == 1)
        self.assertTrue(s.c[1] == 0)

    def test_xor(self):
        """
        Tests the xoring of one row to another
        """
        t = 10
        s = Schedule(t, t)
        self.assertTrue(len(s.xors) == 0)

        # Test xoring row 1 into row 0
        s.xor(0, 1)
        self.assertTrue(len(s.xors) == 1)
        source_row, target_row = s.xors[0]
        self.assertTrue(source_row == 1)
        self.assertTrue(target_row == 0)
