import hashlib
import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chunker import StringChunker

DEFAULT_FILE = 'latin_text'
DEFAULT_K = 4
DEFAULT_SYMBOLSIZE = 1024 * 1024


class TestChunker(unittest.TestCase):

    def get_string(self):
        f = open(DEFAULT_FILE, "r")
        string = f.read()
        f.close()
        return string

    def test_blocks_and_padding(self):
        """
        Calculates the number of blocks and padding on the last block.
        Test then compares those numbers to an actual chunking
        """
        string = self.get_string()
        stringsize = len(string)
        blocksize = DEFAULT_K * DEFAULT_SYMBOLSIZE
        total_blocks = int(math.ceil(stringsize / (blocksize * 1.0)))
        padding_size = blocksize - (stringsize % blocksize)

        with StringChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, string) as chunker:

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

            # Continuing to chunk should return none, because
            # in theory, we have chunked exactly total_blocks
            self.assertIsNone(chunker.chunk())

    def test_symbols(self):
        """
        Chunks all of a string and ensures that every
        chunk has the same number of symbols and that each symbol
        is of length symbolsize
        """
        string = self.get_string()
        with StringChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, string) as chunker:
            chunk = chunker.chunk()
            symbol_length_in_uints = DEFAULT_SYMBOLSIZE / chunker.bytes_per_int
            while(chunk):
                self.assertTrue(len(chunk) == DEFAULT_K)
                for s in chunk:
                    self.assertTrue(len(s) == symbol_length_in_uints)
                chunk = chunker.chunk()

    def test_content(self):
        """
        Tests that the content 0 padding of all blocks has the same md5 as
        the original content
        """

        string = self.get_string()
        md5 = hashlib.md5(string)
        original_digest = md5.hexdigest()

        new_string = ""
        with StringChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, string) as chunker:
            chunk = chunker.chunk()
            while(chunk):
                for symbol in chunk:
                    new_string += symbol.tostring()
                if chunk.padding > 0:
                    new_string = new_string[:-(chunk.padding)]
                chunk = chunker.chunk()

        md5 = hashlib.md5(new_string)
        new_digest = md5.hexdigest()
        self.assertEqual(original_digest, new_digest)
