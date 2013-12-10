from hashlib import md5
from ctypes import Structure, c_uint16, c_uint32, c_char

import ctypes

# Compute the digest size
DIGEST_SIZE = md5().digest_size


class Metadata(Structure):
    """
    Class describing the metadata for a RaptorR10 encoded symbol
    """

    _fields_ = [
        ("esi", c_uint32),
        ("k", c_uint16),
        ("padding", c_uint32),
        ("hash", c_char * DIGEST_SIZE)
    ]

    def __str__(self):
        """
        Override the default __str__ method with this one.

        Returns a string
        """
        return str(buffer(self))

    @classmethod
    def fromstring(cls, string):
        """
        Creates a metadata instance from a string.
        Assumes metadata is at the beginning of the string.
        The string is then sliced into two parts, the first containing
        the metadata and the second containing the rest of the string

        Arguments:
        string -- String containing at least enough bytes for the metadata

        returns a 2 tuple (metadata, restofstring)
        """
        meta = cls()
        meta_length = len(str(buffer(meta)))

        # Break string into the meta portion of the string
        # and the rest of the string
        meta_string = string[:meta_length]
        string = string[meta_length:]

        # Move
        ctypes.memmove(ctypes.addressof(meta), meta_string, meta_length)
        return (meta, string)
