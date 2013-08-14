import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from chunker import Chunker, SymbolSizeException

DEFAULT_SYMBOLSIZE = 64
DEFAULT_K = 10
DEFAULT_STREAM = None

class TestChunker(unittest.TestCase):

    def test_chunker_init(self):
        """
        Tests the basic initialization of the chunker class
        """
        expected_blocksize = DEFAULT_SYMBOLSIZE * DEFAULT_K
        expected_block_id = 0
        c = Chunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_STREAM)

        # Check k
        self.assertEqual(c.k, DEFAULT_K)

        # Check Symbolsize
        self.assertEqual(c.symbolsize, DEFAULT_SYMBOLSIZE)

        # Check blocksize
        self.assertEqual(c.blocksize, expected_blocksize)

        # Check expected block id
        self.assertEqual(c.block_id, expected_block_id)

    def test_64bit_init(self):
        """
        Tests the initialization of the chunker on 64 bit systems
        """
        original = config._64BIT
        config._64BIT = True
        try:
            c = Chunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_STREAM)
            self.assertEqual(c.dtype, "uint64")
            self.assertEqual(c.bytes_per_int, 8)
        finally:
            config._64BIT = original

    def test_32bit_init(self):
        """
        Tests the initialization of the chunker on 32 bit systems
        """
        original = config._64BIT
        config._64BIT = False
        try:
            c = Chunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_STREAM)
            self.assertEqual(c.dtype, "uint32")
            self.assertEqual(c.bytes_per_int, 4)
        finally:
            config._64BIT = original

    def test_block_ids(self):
        """
        Tests the generation of block ids
        The first should be 0
        The second should be 0 + 1
        """
        c = Chunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_STREAM)
        expected_block_id = 0

        # Check that first blockid = 0
        self.assertEqual(c.get_block_id(), expected_block_id)

        # Check that the next block id = 1
        expected_block_id = 1
        self.assertEqual(c.get_block_id(), expected_block_id)
        
    
    def test_64bit_symbolsize(self):

        """
        Asserts that SymbolSizeExceptions are raised for invalid symbol sizes
        on 64 bit systems

        A good symbolsize for 64 bit is in increments of 8 BYTES
        """

        #save the original
        original = config._64BIT

        try:
            config._64BIT = True

            # Try a bad symbolsize.   
            with self.assertRaises(SymbolSizeException):
                c = Chunker(10, 7, DEFAULT_STREAM)

            try:
                # Try a good symbol size (exactly 8 BYTES)
                c = Chunker(10, 8, DEFAULT_STREAM)

                # Try a multiple of 8BYTES
                c = Chunker(10, 24, DEFAULT_STREAM)
            except Exception, e:
                self.fail(e.tostring())
            
        finally:
            # Restore original
            config._64BIT = original

    def test_32bit_symbolsize(self):

        """
        Asserts that SymbolSizeExceptions are raised for invalid symbol sizes
        on 32 bit systems

        A good symbolsize for 32 bit is in increments of 4 BYTES
        """

        #save the original
        original = config._64BIT

        try:
            config._64BIT = False
            # Try a bad symbolsize.   
            with self.assertRaises(SymbolSizeException):
                c = Chunker(10, 3, DEFAULT_STREAM)

            try:
                # Try a good symbol size (exactly 4 BYTES)
                c = Chunker(10, 4, DEFAULT_STREAM)

                # Try a multiple of 4 BYTES
                c = Chunker(10, 16, DEFAULT_STREAM)
            except Exception, e:
                self.fail(e.tostring())
            
        finally:
            # Restore original
            config._64BIT = original
