"""
Copyright [2013] [James Absalon]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import io
import os
import config
from cStringIO import StringIO as StringIO
from block import Source as SourceBlock

class SymbolSizeException(Exception):

    def __init__(self, bits, _bytes):
    
        """
        Exception for when symbolsizes are not suitable for architecture

        Arguments:
        bits -- Integer number of bits in a register (Usually 32, 64)
        _bytes -- Number of bytes per register (64bit is 8 bytes and so forth)
        """
        message = "Symbol size must be a multiple of %s bytes for %s bit systems." % (_bytes, bits)
        super(SymbolSizeException, self).__init__(message)

class Chunker(object):
    
    def __init__(self, k, symbolsize):
        """
        Constructor for initializing the base Chunker

        Arguments:
        k -- Integer number of symbols per block
        symbolsize -- Integer number of BYTES per symbol.
        """
        self.block_id = 0
        self.k = k
        self.symbolsize = symbolsize
        self.blocksize = self.symbolsize * self.k
        
        # Check for 64 bit
        if config._64BIT:
            if not (self.symbolsize % 8 == 0):
                raise SymbolSizeException(64, 64 / 8)
            self.bytes_per_int = 8
            self.dtype = "uint64"

        # Check for 32 bit
        else:
            if not (self.symbolsize % 4 == 0):
                raise SymbolSizeException(32, 32 / 8)
            self.bytes_per_int = 4
            self.dtype = "uint32"

        self.ints_to_read = self.symbolsize / self.bytes_per_int

    def get_block_id(self):
        """
        Gets the current block id and increments to prepare for the next block.
        Returns the current block id
        """
        r = self.block_id
        self.block_id += 1
        return r

    def __enter__(self):
        """
        For use within a with block
        """
        return self
    
    def __exit__(self, type, value, traceback):
        """
        Does nothing when exiting the with context
        """
        pass

class FileChunker(Chunker):

    def __init__(self, k, symbolsize, filename):
        """
        File chunker constructor

        Arguments:
        k           -- Integer number of symbols per block
        symbol_size -- Integer Size of each symbol (IN BYTES)
        filename    -- String name of file to chunk
        """
        super(FileChunker, self).__init__(k, symbolsize)
        self.filename = filename
        self.filesize = os.path.getsize(filename)

        try:
            self._f = io.open(filename, 'rb')
        except Exception:
            raise Exception('Unable to open file %s for reading.' % filename)

    def __exit__(self, type, value, traceback):
        """
        Automatically attempts to close the file upon exiting the with context
        """
        self.close()

    def chunk(self):
        """
        Should return a block of strings
        Attempts to read k symbols from the file and pads a block
        so that the block is k symbols of symbolsize * 8 bits
        """
        # Check to see file is still open
        if self._f.closed:
            return None
        
        block = SourceBlock(self.k, self.symbolsize, self.get_block_id())

        j = 0
        EOF = False

        while (j < self.k and not EOF):
            b = self._read()
            if not (b is None):
                block.append(b)
                j += 1
            else:
                EOF = True
                self.close()

        if len(block) == 0:
            return None

        block.pad()
        return block

    def _read(self):
        """
        Reads symbolsize bytes from the file
        Returns None if the length is 0
        Returns a string otherwise
        """

        s = self._f.read(self.symbolsize)
        if not len(s):
            return None
        return s

    def close(self):
        """
        Attempts to close the file associated with this chunker
        """
        try:
            self._f.close()
        except:
            pass

class StringChunker(Chunker):
    """
    Chunks large strings into smaller parts similar
    to the file chunker
    """

    def __init__(self, k, symbolsize, value):
        """
        Initialized the string chunker

        Arguments:
        k -- Integer number of symbols per chunk
        symbolsize -- Size of each symbol in a chunk]
        value -- String to chunk
        """
        super(StringChunker, self).__init__(k, symbolsize)
        self.value = value
        self.bytesread = 0
        self.stringsize = len(value)
        self.stream = StringIO(value)

    def __enter__(self):
        return self 

    def __exit__(self, type, value, traceback):
        self.close()

    def chunk(self):
        """
        Should return a block of strings
        Attempts to read k symbols from the file and pads a block
        so that the block is k symbols of symbolsize bytes
        """

        if self.bytesread >= self.stringsize:
            return None

        block = SourceBlock(self.k, self.symbolsize, self.get_block_id())

        j = 0
        while j < self.k and self.bytesread < self.stringsize:
            b = self._read()
            if not (b is None):
                block.append(b)
                j += 1
            else:
                break

        if len(block) == 0:
            return None

        block.pad()
        return block
    
    def _read(self):
        """
        Reads symbolsize bytes from the file
        Returns None if the length is 0
        Returns a string of length symbolsize unless there aren't enough bytes
        to create a complete symbol
        """

        s = self.stream.read(self.symbolsize)
        if not len(s):
            return None
        return s

    def close(self):
        try:
            self.stream.close()
        except:
            pass
