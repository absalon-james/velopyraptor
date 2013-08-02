import math
import os
import sys
import unittest

from bitarray import bitarray

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matrix

class TestMatrix(unittest.TestCase):

    def random_matrix(self, rows, columns):
        """
        Creates a random rows x columns matrix

        Returns a list of bitarrays
        """
        m = []
        for i in xrange(rows):
            m.append(bitarray(columns))
        return m

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

    def test_inverse_bad_dimensions(self):
        """
        Tests trying to get the inverse of a non square matrix
        """
        rows = 5
        columns = 6
        m = []
        for i in xrange(rows):
            m.append(bitarray(columns))

        with self.assertRaises(Exception):
            m_inverse = matrix.inverse(m)

    def test_inverse_2x2(self):
        """
        Tests the computation of a simple 2x2 matrix
        """
        m = [bitarray('11'), bitarray('10')]
        known_inverse = [bitarray('01'), bitarray('11')]
        m_inverse = matrix.inverse(m)

        # Make sure m isnt changed
        self.assertTrue(m[0] == bitarray('11'))
        self.assertTrue(m[1] == bitarray('10'))

        # Make sure inverse result has same dimensions
        self.assertTrue(len(m) == len(m_inverse))
        for i in xrange(len(m)):
            self.assertTrue(len(m[i]) == len(m_inverse[i]))

        # Make sure result is same as known result
        for i in xrange(len(known_inverse)):
            self.assertTrue(m_inverse[i] == known_inverse[i])

    def test_multiply_bad_dimensions(self):
        """
        Tests the multiplication of two matrices using
        incompatible dimensions
        """
        outer = 4
        inner = 5
        a = self.random_matrix(outer, inner)
        b = self.random_matrix(outer, inner)

        # Attempt to multiply 4x5 by 4x5 (should fail)
        with self.assertRaises(Exception):
            c = matrix.multiply(a, b)

    def test_good_dimensions(self):
        """
        Tests that dimensions are correct on result matrix
        from multiplying two matrices together
        """
        outer = 4
        inner = 5
        a = self.random_matrix(outer, inner)
        b = self.random_matrix(inner, outer)
        c = matrix.multiply(a, b)

        # c should now be a 4 x 4 matrix
        self.assertTrue(len(c) == outer)
        for row in c:
            self.assertTrue(len(row) == outer)

    def test_inverse_multiply(self):
        """
        Checks that multiplying a matrix by its inverse
        is the identity
        """
        a = [bitarray('11'), bitarray('10')]
        a_inverse = matrix.inverse(a)
        identity = matrix.identity(2)
        result = matrix.multiply(a, a_inverse)
        # Make sure the result matches the identity
        for i in xrange(len(identity)):
            self.assertTrue(result[i] == identity[i])

    def test_rank_2x2_zeros(self):
        """
        Tests that a 2x2 zero matrix's rank is 0
        """
        m = [bitarray("00"), bitarray("00")]
        self.assertTrue(matrix.rank(m) == 0)

    def test_rank_2x2_identity(self):
        """
        Tests that a 2x2 identity matrix's rank is 2
        """
        m = [bitarray("10"), bitarray("01")]
        self.assertTrue(matrix.rank(m) == 2)

    def test_rank_2x2_duplicate(self):
        """
        Tests that a 2x2 matrix with two non zero rows
        that are identical have a rank of 1
        """
        m = [bitarray("10"), bitarray("10")]
        rank = matrix.rank(m)
        self.assertTrue(matrix.rank(m) == 1)

    def test_rank_5x5_partial_identity(self):
        """
        Tests that a 5x5 partial identity matrix's rank
        is the number of non zero rows
        """
        m = [bitarray("10000"),
             bitarray("00000"),
             bitarray("00000"),
             bitarray("00000"),
             bitarray("00001")]
        self.assertTrue(matrix.rank(m) == 2)
