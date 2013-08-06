import os
import sys
import unittest

from hashlib import md5

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metadata import Metadata

HASH_STRING = "This is a test string.  Please compute the md5"
ESI = 30
K = 10
PADDING = 20
DIGEST = md5(HASH_STRING).digest()

class TestMetadata(unittest.TestCase):
    """
    Collection of tests for the metadata module
    """

    def test_init(self):
        """
        Tests that known fields init in the right order
        and to the expected value
        """

        meta = Metadata(ESI, K, PADDING, DIGEST)
        self.assertTrue(meta.esi == ESI)
        self.assertTrue(meta.k == K)
        self.assertTrue(meta.padding == PADDING)
        self.assertTrue(meta.hash == DIGEST)
        
    def test_esi_range(self):
        """
        Tests the number ranges for the esi field
        """
        # There are 4294967296 ints in a 32 bit integer

        # Hitting that number exactly should overflow the integer back to 0
        self.assertTrue(Metadata(4294967296).esi == 0)

        # Going over by two should overflow to 1
        self.assertTrue(Metadata(4294967297).esi == 1)

        # Staying under 4294967296 should stay the same
        self.assertTrue(Metadata(4294967295).esi == 4294967295)

        # Zero should work as expected
        self.assertTrue(Metadata(0).esi == 0)

        # Negatives should roll backwards
        self.assertTrue(Metadata(-1).esi == 4294967295)

    def test_k_range(self):
        """
        Tests the number ranges for the k field
        """
        # There are 65536 possible integers in a 16 bit integer
        # 0 to 65535

        # Hitting 65536 should overflow to 0
        self.assertTrue(Metadata(0, 65536).k == 0)

        # Going over by two should overflow to 1
        self.assertTrue(Metadata(0, 65537).k == 1)

        # Staying under 65536 should work as expected
        self.assertTrue(Metadata(0, 65535).k == 65535)

        # Zero should work as expected
        self.assertTrue(Metadata(0, 0).k == 0)

        # Negatives should roll backwards
        self.assertTrue(Metadata(0, -1).k == 65535)

    def test_padding_range(self):
        """
        Tests the number ranges for the padding field
        """
        # There are 4294967296 ints in a 32 bit integer

        # Hitting that number exactly should overflow the integer back to 0
        self.assertTrue(Metadata(0, 0, 4294967296).padding == 0)

        # Going over by two should overflow to 1
        self.assertTrue(Metadata(0, 0, 4294967297).padding == 1)

        # Staying under 4294967296 should stay the same
        self.assertTrue(Metadata(0, 0, 4294967295).padding == 4294967295)

        # Zero should work as expected
        self.assertTrue(Metadata(0, 0, 0).padding == 0)

        # Negatives should roll backwards
        self.assertTrue(Metadata(0, 0, -1).padding == 4294967295)

    def test_hash_length(self):
        """
        Tests the length of the md5 hash
        """
        meta = Metadata(0, 0, 0, DIGEST)
        self.assertTrue(len(DIGEST) == len(meta.hash))
