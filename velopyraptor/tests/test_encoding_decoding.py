import hashlib
import math
import io
import os
import sys
import unittest

# Parent holds the encoding/decoding python files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chunker import FileChunker
from encoder import Encoder
from decoder import Decoder

DEFAULT_FILE = 'latin_text'
SYMBOLSIZE = 1024 * 100

class TestEncodingDecoding(unittest.TestCase):

    def setUp(self):
        """
        Read entire test file one KB at a time
        and determine the md5 of the content
        for comparison to encoding and decoding
        """
        md5 = hashlib.md5()
        f = io.open(DEFAULT_FILE, 'r+b')
        chunk = f.read(SYMBOLSIZE)
        while not chunk == "":
            md5.update(chunk)
            chunk = f.read(SYMBOLSIZE)
        f.close()

        self.original_digest = md5.hexdigest()

    def test_with_all_k_s(self):

        k_min = 4
        k_max = 20

        ks_that_fail = []

        for i in xrange(k_min, k_max + 1):
            try:
                if not self.encode_decode(i):
                    print "K: %s failed" % i
                    ks_that_fail.append(i)
                else:
                    print "K %s passed" % i
            except Exception, e:
                ks_that_fail.append(i)
                print "K: %s failed" % i
                print e

        if len(ks_that_fail) > 0:
            self.fail("K Failed for the following values: %s" % ks_that_fail)

    def encode_decode(self, k):

        print "\nTesting encoding and then decoding with k = %s" % k

        md5 = hashlib.md5()

        with FileChunker(k, SYMBOLSIZE, DEFAULT_FILE) as chunker:
        
            chunk = chunker.chunk()
            while chunk:
                padding = chunk.padding

                symbols = [(i, chunk[i]) for i in xrange(k)]
                encoder = Encoder(k, symbols)
                symbols = []

                # Start at k/2 and produce 1.25k more symbols to get a mix
                # of parity and source symbols
                for i in xrange(k * 2):
                    symbols.append(encoder.next())

                encoder = None
                decoder = Decoder(k)
                for tup in symbols:
                    decoder.append(tup)

                decoder.decode()
                decoded = bytearray()
                for i in xrange(k):
                    esi, s = decoder.next()
                    decoded += s.tostring()
                decoder = None

                if padding:
                    padding = 0 - padding
                    print "Removing padding", padding, "bytes"
                    decoded = decoded[:padding]

                md5.update(decoded)
            
                # Continue on to the next chunk
                chunk = chunker.chunk()

        print "Original digest:", self.original_digest
        print "Decoded digest:", md5.hexdigest()
        return self.original_digest == md5.hexdigest()
