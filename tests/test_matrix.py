import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matrix

class TestMatrix(unittest.TestCase):

    def test_zeros(self):
        """
        Test the zeros matrix method
        """
        rows = 5
        columns = 10
        # Get 5 rows of 10 bits
        m = matrix.zeros(rows, columns)

        # Make sure we have rows rows
        self.assertTrue(len(m) == rows)

        for row in xrange(rows):
            # Make sure each row has columns bits
            self.assertTrue(len(m[row]) == columns)

            # Make sure each bit in row row is 0(False)
            for i in xrange(columns):
                self.assertTrue(m[row][i] == False)

    def test_identity(self):
        """
        Tests the identity matrix creation method
        """
        rows_and_columns = 5

        # Get a 5x5 identity matrix
        m = matrix.identity(rows_and_columns)

        # Make sure there are rows_and_columns rows
        self.assertTrue(len(m) == rows_and_columns)
        for row in xrange(rows_and_columns):
            # Make sure each row has rows_and_columns columns
            self.assertTrue(len(m[row]) == rows_and_columns)

            # Make sure the row'th column in row row is a 1
            self.assertTrue(m[row][row] == True)

            # Make sure that each row has exactly 1 one 1
            self.assertTrue(m[row].count() == 1)

