import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chunker import FileChunker

DEFAULT_FILE = 'latin_text'
DEFAULT_K = 4
DEFAULT_SYMBOLSIZE = 1024 * 1024

class TestChunker(unittest.TestCase):

    def get_chunker(self, k=DEFAULT_K, symbolsize=DEFAULT_SYMBOLSIZE, filename=DEFAULT_FILE):
        """
        Returns a chunker.
        """
        return FileChunker(k, symbolsize, filename)

    def test_non_file(self):
        """
        Asserts that an exception is raised when attempting
        to chunk a non file
        """
        with self.assertRaises(Exception):
            filename = 'somebadfiledfsgdsgsdfg.txt'
            chunker = self.get_chunker(filename=filename)

    def test_good_file(self):
        """
        Asserts that a good file can be opened
        """        
        try:
            chunker = self.get_chunker()
            chunker.close()
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

        # Grab a chunker
        chunker = self.get_chunker()

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

        # Close the chunker
        chunker.close()

    def test_symbols(self):
        """
        Chunks all of a file and ensure that every
        chunk has the same number of symbols anmd that each symbol
        is of length symbolsize
        """
        chunker = self.get_chunker()
        chunk = chunker.chunk()
        symbol_length_in_bits = DEFAULT_SYMBOLSIZE * 8
        while(chunk):
            self.assertTrue(len(chunk) == DEFAULT_K)

            # Check each symbol to ensure it is symbolsize * 8 bits long
            for s in chunk:
                self.assertTrue(len(s) == symbol_length_in_bits)
            chunk = chunker.chunk()
        chunker.close()
