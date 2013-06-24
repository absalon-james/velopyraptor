import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from distributions.half import choose
from decoder import Decoder
from raptor import RaptorR10ParameterException

class TestK(unittest.TestCase):

    def test_less_than_min_k(self):
        """
        Makes sure trying to use a k < 4 fails
        """
        with self.assertRaises(RaptorR10ParameterException):
            d = Decoder(3)

    def test_min_k(self):
        """
        Makes sure using the minimum k works
        """
        try:
            d = Decoder(4)
        except RaptorR10ParamterException:
            self.fail("Using k = 4 failed")

    def test_more_than_max_k(self):
        """
        Makes sure trying to use a k > 8192 fails
        """
        with self.assertRaises(RaptorR10ParameterException):
            d = Decoder(8193)

    def test_max_k(self):
        """
        Makes sure k at max works
        """
        try:
            d = Decoder(8192)
        except RaptorR10ParameterException:
            self.fail("Using k = 8192 fails")
            
    def test_all_k(self):
        """
        Tests all valid values of k
        """
        try:
            for i in xrange(4, 8192):
                d = Decoder(i)

                # Check that x is >= 2k
                self.assertTrue(d.x * (d.x - 1) >= 2 * d.k)

                # Check that S >= ceil(0.01 * k) + X
                self.assertTrue(d.s >= (math.ceil(0.01 * d.k) + d.x))

                # Check that H choose H / 2 >= K + S
                self.assertTrue(choose(d.h, int(math.ceil(d.h / 2.00))) >= d.k + d.s)

                # Check that H' = ceil(H/2)
                self.assertTrue(d.h_prime == math.ceil(d.h / 2.00))

                # Check that k + s + h = l
                self.assertTrue(d.k + d.s + d.h == d.l)

                # Check that l_prime >= l
                self.assertTrue(d.l_prime >= d.l)

        except RaptorR10ParameterException:
            self.fail('Using k = %s fails' % i)
