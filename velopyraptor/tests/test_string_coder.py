import copy
import hashlib
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from metadata import Metadata
from string_coder import StringEncoder, StringDecoder

DEFAULT_K = 10


class TestStringEncoder(unittest.TestCase):

    def test_padding_0_length(self):
        """
        Tests the padding of a string of length 0
        """
        string = ""
        coder = StringEncoder(DEFAULT_K, string)
        self.assertTrue(coder.padding == 0)

    def test_padding_1_length(self):
        """
        Tests the padding of a string of length 1
        """
        string = os.urandom(1)
        coder = StringEncoder(DEFAULT_K, string)
        expected_padding = (DEFAULT_K * config.alignment) - 1
        self.assertTrue(coder.padding == expected_padding)

    def test_even_padded_length(self):
        """
        Tests the padding on a string that should not need padding
        """
        length = DEFAULT_K * config.alignment
        string = os.urandom(length)
        coder = StringEncoder(DEFAULT_K, string)
        self.assertTrue(coder.padding == 0)

    def test_k_symbols(self):
        """
        Tests that symbolfy produces k symbols and that all
        k symbols are the same length
        """
        length = DEFAULT_K * config.alignment
        string = os.urandom(length)
        coder = StringEncoder(DEFAULT_K, string)
        symbols = coder.symbolfy(string)
        self.assertTrue(len(symbols) == DEFAULT_K)
        for esi, symbol in symbols:
            self.assertTrue(len(symbol) == 1)

    def test_symbols(self):
        """
        Tests that symbols are sliced correctly
        """
        string = os.urandom(999)
        digest = hashlib.md5(string).digest()
        coder = StringEncoder(DEFAULT_K, string)

        symbols = coder.symbolfy(string)
        padding = coder.padding
        reassembled = ""

        for esi, symbol in symbols:
            part = symbol.tostring()
            reassembled += part

        if padding:
            reassembled = reassembled[:-padding]

        new_digest = hashlib.md5(reassembled).digest()
        self.assertTrue(digest == new_digest)

    def test_next_type(self):
        """
        Tests the type returned by the next method of the string encoder
        """
        string = os.urandom(999)
        coder = StringEncoder(DEFAULT_K, string)
        for i in xrange(2 * DEFAULT_K):
            self.assertTrue(str == type(coder.next()))


class TestStringDecoder(unittest.TestCase):

    def get_random_symbols(self, size, padding):
        """
        Produces a symbol string with metadata of size size
        and sets the metadata's padding to padding

        Arguments:
        size -- Integer number of bytes (should be aligned)
        padding -- Integer number of padding bytes

        Returns list of strings
        """
        symbols = []
        for i in xrange(DEFAULT_K):
            string = os.urandom(size)
            meta = Metadata(i,
                            DEFAULT_K,
                            padding, hashlib.md5(string).digest())
            symbols.append("%s%s" % (str(meta), string))
        return symbols

    def test_meta_init(self):
        """
        Tests that ther coder chooses the same k and padding
        as is encoded in the metadata for each symbol
        """
        padding = 10
        size = 80
        symbols = self.get_random_symbols(size, padding)
        coder = StringDecoder(symbols)
        self.assertTrue(DEFAULT_K == coder.k)
        self.assertTrue(padding == coder.padding)
        self.assertIsNotNone(coder.i_symbols)

    def test_bad_k(self):
        """
        Simulates bad metadata value for k on one symbol
        """
        size = 80
        padding = 10
        symbols = self.get_random_symbols(size, padding)
        meta, symbol = Metadata.fromstring(symbols[0])
        meta.k = DEFAULT_K + 1
        symbols[0] = "%s%s" % (str(meta), symbol)
        with self.assertRaises(Exception):
            StringDecoder(symbols)

    def test_bad_padding(self):
        """
        Simulates bad metadata value for padding on one symbol
        """
        size = 80
        padding = 10
        symbols = self.get_random_symbols(size, padding)
        meta, symbol = Metadata.fromstring(symbols[0])
        meta.padding = padding + 1
        symbols[0] = "%s%s" % (str(meta), symbol)
        with self.assertRaises(Exception):
            StringDecoder(symbols)

    def test_no_symbols(self):
        """
        Simulates trying to decode an empty list
        """
        symbols = []
        with self.assertRaises(Exception):
            StringDecoder(symbols)

    def test_linearly_dependent_symbols(self):
        """
        Simulates a situation that results in an all zero row in matrix a
        while decoding
        """
        size = 80
        padding = 10
        symbols = self.get_random_symbols(size, padding)
        symbols[0] = copy.deepcopy(symbols[1])
        with self.assertRaises(Exception):
            StringDecoder(symbols)

    def test_decoding(self):
        """
        Tests encoding a string and then decoding a string
        """
        size = 1000
        string = os.urandom(size)
        original_md5 = hashlib.md5(string).digest()
        coder = StringEncoder(DEFAULT_K, string)
        symbols = [coder.next() for i in xrange(DEFAULT_K * 2)]
        coder = StringDecoder(symbols)
        string = coder.decode()

        # Test the size
        self.assertTrue(len(string) == size)

        # Test the md5 digest
        self.assertTrue(original_md5 == hashlib.md5(string).digest())
