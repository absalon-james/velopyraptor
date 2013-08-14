import hashlib
import math
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from chunker import FileChunker

DEFAULT_FILE = 'latin_text'
DEFAULT_K = 4
DEFAULT_SYMBOLSIZE = 1024 * 100

class TestFileChunker(unittest.TestCase):

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

            # Continuing to chunk should return none, because
            # in theory, we have chunked exactly total_blocks
            self.assertIsNone(chunker.chunk())

    def test_symbols(self):
        """
        Chunks all of a file and ensure that every
        chunk has the same number of symbols and that each symbol
        is of length symbolsize
        """
        with FileChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_FILE) as chunker:
            chunk = chunker.chunk()
            while(chunk):
                self.assertTrue(len(chunk) == DEFAULT_K)
                # Check each symbol to ensure it is symbolsize / 8 uint64s long
                for s in chunk:
                    self.assertTrue(len(s) == DEFAULT_SYMBOLSIZE)
                chunk = chunker.chunk()

    def test_content(self):
        """
        Tests the content of the string is the same as the content
        of the chunked string minus the padding
        """
        f = open(DEFAULT_FILE)
        string = f.read()
        f.close()
        md5 = hashlib.md5(string)
        original_digest = md5.hexdigest()

        new_string = ""
        with FileChunker(DEFAULT_K, DEFAULT_SYMBOLSIZE, DEFAULT_FILE) as chunker:
            chunk = chunker.chunk()
            while(chunk):
                for symbol in chunk:
                    new_string += symbol
                if chunk.padding > 0:
                    new_string = new_string[:-(chunk.padding)]
                chunk = chunker.chunk()

        md5 = hashlib.md5(new_string)
        new_digest = md5.hexdigest()
        self.assertEqual(original_digest, new_digest)

