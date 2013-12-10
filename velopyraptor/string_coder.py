import config
import hashlib
import numpy
from metadata import Metadata
from raptor import RaptorR10


class StringEncoder(RaptorR10):
    """
    Used to encode a single string without chunking by breaking it
    into k source parts and calculating intermediate symbols from it
    """

    def __init__(self, k, to_encode, **kwargs):
        """
        Arguments:
        k -- Integer number of source symbols
        to_encode -- String to encode
        """
        super(StringEncoder, self).__init__(k, **kwargs)
        self.padding = 0
        self.symbols = self.symbolfy(to_encode)
        self.calculate_i_symbols()

    def pad(self, to_encode):
        """
        Pad the string until we can have k even length strings
        that are also in multiples of 4(32 bit) or 8(64 bit) bytes
        """

        if config._64BIT:
            alignment = 8
        else:
            alignment = 4

        length = len(to_encode)
        padding = 0

        # Determine how many bytes needed to make an even k
        if length % self.k:
            padding = self.k - (length % self.k)

        # Determine how many bytes to add to each symbol to have multiples
        # of the alignment
        padding_per_symbol = (length + padding) / self.k
        if padding_per_symbol % alignment:
            padding_per_symbol = alignment - (padding_per_symbol % alignment)
            padding += padding_per_symbol * self.k

        to_encode = to_encode.ljust(length + padding, "\x00")
        self.padding = padding
        return to_encode

    def symbolfy(self, to_encode):
        """
        Turns to_encode into tuples consisting of
        esi and numpy arrays
        """
        to_encode = self.pad(to_encode)
        symbols = []
        length = len(to_encode)
        step = length / self.k
        for i in xrange(self.k):
            part = to_encode[i * step: (i + 1) * step]
            symbols.append((i, numpy.fromstring(part, dtype=config.dtype)))
        return symbols

    def next(self):
        """
        Converts parent's tuple (esi, numpy array) to
        string prefixed by packed metadata

        Returns string
        """
        esi, symbol = super(StringEncoder, self).next()
        symbol = symbol.tostring()
        digest = hashlib.md5(symbol).digest()
        meta = Metadata(esi, self.k, self.padding, digest)
        return "%s%s" % (str(meta), symbol)


class StringDecoder(RaptorR10):
    """
    Strings are appended to an instance of this class until decoding
    becomes possible at which point the intermediate symbols can
    be calculated
    """

    def __init__(self, strings):
        """
        Breaks meta data off of strings, checks metadata to make sure
        the match, then encodes

        Arguments:
        strings -- List of strings
        """

        symbols = [Metadata.fromstring(s) for s in strings]

        if not len(symbols):
            raise Exception("No symbols were provided to decode")

        # Make sure we have padding and k agreement between all symbols
        self.k = symbols[0][0].k
        self.padding = symbols[0][0].padding
        for meta, symbol in symbols:
            if not (meta.k == self.k):
                raise Exception("Provided symbols do not have k agreement")
            if not (meta.padding == self.padding):
                raise Exception("Provided symbols do not "
                                "have padding agreement")

        # Invoke parent's init to set up raptor coding parameters
        super(StringDecoder, self).__init__(self.k)

        # Actually add symbols until decoding is possible
        for meta, symbol in symbols:
            self.symbols.append((meta.esi,
                                 numpy.fromstring(symbol,
                                                  dtype=config.dtype)))

        if not self.can_decode():
            raise Exception("Unable to decode with the symbols provided.")

        # Calculate i symbols
        self.calculate_i_symbols()

    def next(self):
        """
        Converts parent's tuple (esi, numpy array) to
        string

        Returns string
        """
        esi, symbol = super(StringDecoder, self).next()
        return symbol.tostring()

    def decode(self):
        """
        Decodes the first k symbols into the original symbols
        stripping any padding if necessary

        Return the original string
        """
        # Check the i symbols
        if not self.i_symbols:
            return None

        # Assemble the first k source symbols into one string
        string = "".join([self.next() for i in xrange(self.k)])

        # Strip any padding if necessary
        if self.padding:
            string = string[:-self.padding]

        # String should now be the original string
        return string
