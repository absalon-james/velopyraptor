"""
============
velopyraptor
============
An implementation of rfc 5053 raptor encoding/decoding in python

Greetings. The goal of this repo is to provide an implementation of the raptor
encoder and decoder described by RFC 5053 which can be found at:

    http://tools.ietf.org/html/rfc5053

RFC 5053 describes a rateless systematic encoder.  The first k source symbols
are the same as the first k encoded symbols. The encoded symbols produced
after k can be considered parity symbols.

Encoding and decoding are much the same process.  The goal is to produce the
intermediate symbols from known encoded symbols.

Almost all of the recommendations by rfc 5053 were followed with a small
exception to the raptor decoding process in 

    http://tools.ietf.org/html/rfc5053#section-5.5.2

The third and fourth phase of decoding describe the computation of
a precomputation matrix to reduce the number of XORS on matrix A.  It appears 
as though this will still have the same number of XORS on the source/encoded
symbols as it would doing standard gaussian elimination on matrix A within
the submatrix u-upper.  I have not tested this and cannot say for certain.

Usage:

Choose a k between 4 and 8192.

Symbols are tuples of the encoded symbol id and the ndarray(of uint64s) representation
of the content. An encoded symbol id < k indicates a source symbol.
"""

from velopyraptor.encoder import Encoder
from bitarray import bitarray
import numpy

# Choose a k
k = 4

dtype = "uint64"

# Choose some source
source = [(0, numpy.fromstring("testtestabcdefgh", dtype=dtype)),
          (1, numpy.fromstring("esttestabcdefght", dtype=dtype)),
          (2, numpy.fromstring("sttestabcdefghte", dtype=dtype)),
          (3, numpy.fromstring("ttestabcdefghtes", dtype=dtype))]

# Create the encoder
encoder = Encoder(k, source)

symbols = []

# Make the first k encoded symbols(also same as source)
print "\nThe first k encoded symbols"
for i in xrange(k):
    esi, symbol = encoder.next()
    print "%s -- %s" % (esi, symbol.tostring())
    symbols.append((esi, symbol))

# Make k more encoded symbols(parity symbols)
for i in xrange(k, 2 * k):
    esi, symbol = encoder.next()
    symbols.append((esi, symbol))

# Stuff was encoded using k = 4
from velopyraptor.decoder import Decoder
k = 4

decoder = Decoder(k)
for esi, symbol in symbols:
    # Only use half of the total symbols to simulate loss/failures
    if esi % 2 == 1:
        decoder.append((esi, symbol))

# Once we are satisfied we have enough symbols we instruct
# the decoder to decode the intermediate symbols
decoder.decode()

# We encode to get the first k encoded symbols which are also
# the source symbols
print "\nDecoding the source symbols"
for i in xrange(k):
    esi, symbol = decoder.next()
    print "%s -- %s" % (esi, symbol.tostring())

"""
This code has not been profiled for optimization yet.
"""
