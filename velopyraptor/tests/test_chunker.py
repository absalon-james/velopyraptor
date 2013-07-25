import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from chunker import Chunker, FileChunker, SymbolSizeException

DEFAULT_FILE = 'latin_text'
DEFAULT_K = 4
DEFAULT_SYMBOLSIZE = 1024 * 1024

class TestChunker(unittest.TestCase):

    def test_symbolsize(self):
        """
        Asserts that SymbolSizeExceptions are raised for improper symbol sizes
        on both 32 bit and 64 bit systems
        """
        # Save original value
        original = config._64BIT

        try:
            # Try a bad symbol size assuming 64 bit
            with self.assertRaises(SymbolSizeException):
                config._64BIT = True
                c = Chunker(10, 7)

            # Try a bad symbolsize assuming 32 bit
            with self.assertRaises(SymbolSizeException):
                config._64BIT = False
                c = Chunker(10, 5)

            # Try a good symbol size
            try:
                config._64BIT = True
                c = Chunker(10, 8)
            except Exception, e:
                self.fail(e.tostring())
                
        # Always reset config value to normal
        finally:
            config._64BIT = original

    def test_non_file(self):
        """
        Asserts that an exception is raised when attempting
        to chunk a non file
        """
        with self.assertRaises(Exception):
            filename = 'somebadfiledfsgdsgsdfg.txt'
            with FileChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, filename) as chunker:
                pass            

    def test_good_file(self):
        """
        Asserts that a good file can be opened
        """
        try:
            with FileChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_FILE) as chunker:
                pass
        except Exception:
            self.fail("Unable to open %s for chunking" % (DEFAULT_FILE))

    def test_blocks_and_padding(self):
        """
        Calculates the number of blocks and padding on the last block.
        Test then compares those numbers to an actual chunking
        """
        filesize = os.path.getsize(DEFAULT_FILE)
        blocksize = DEFAULT_K * DEFAULT_SYMBOLSIZE
        total_blocks = int(math.ceil(filesize / (blocksize * 1.0)))
        padding_size = blocksize - (filesize % blocksize)

        with FileChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_FILE) as chunker:

            for i in xrange(total_blocks):
                chunk = chunker.chunk()

                # We chould have a chunk for all i
                self.assertIsNotNone(chunk)

                # Assert that the last block has padding
                if i == total_blocks - 1:
                    self.assertTrue(chunk.padding == padding_size)

                # And all others do not
                else:
                    self.assertTrue(chunk.padding == 0)

            # Continueing to chunk should return none, because
            # in theory, we have chunked exactly total_blocks
            self.assertIsNone(chunker.chunk())

    def test_symbols(self):
        """
        Chunks all of a file and ensure that every
        chunk has the same number of symbols anmd that each symbol
        is of length symbolsize
        """
        with FileChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_FILE) as chunker:
            chunk = chunker.chunk()
            symbol_length_in_uint64s = DEFAULT_SYMBOLSIZE / 8 # uint64 for 64 bit systems
            #symbol_length_in_uint32s = DEFAULT_SYMBOLSIZE / 4 # uint32 for 32 bit systems
            while(chunk):
                self.assertTrue(len(chunk) == DEFAULT_K)

                # Check each symbol to ensure it is symbolsize / 8 uint64s long
                for s in chunk:
                    self.assertTrue(len(s) == symbol_length_in_uint64s)
                chunk = chunker.chunk()
