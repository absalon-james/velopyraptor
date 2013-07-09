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
import numpy
import os
import config
from block import Source as SourceBlock

class FileChunker(object):

    def __init__(self, k, symbolsize, filename):
        """
        File chunker constructor

        Arguments:
        k           -- Integer number of symbols per block
        symbol_size -- Integer Size of each symbol (IN BYTES)
        filename    -- String name of file to chunk
        """
        self.block_id = 0
        self.k = k
        self.symbolsize = symbolsize # Bytes
        self.blocksize = self.symbolsize * self.k # Bytes
        self.filename = filename
        self.filesize = os.path.getsize(filename)

        # Check for 64 bit
        if config._64BIT:
            if not (self.symbolsize % 8 == 0):
                raise Exception("Please choose a symbol size that is a multiple of 8 Bytes for 64 bit systems")
            self.ints_to_read = self.symbolsize / 8 
            self.dtype = "uint64"

        # Check for 32 bit
        else:
            if not (self.symbolsize % 4 == 0):
                raise Exception("Please choose a symbol size that is a multiple of 4 Bytes for 32 bit systems")
            self.ints_to_read = self.symbolsize / 4
            self.dtype = "uint32"

        try:
            self._f = open(filename, 'rb')
        except Exception:
            raise Exception('Unable to open file %s for reading.' % filename)

    def __enter__(self):
        """
        For use within a with block
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Automatically attempts to close the file upon exiting the with context
        """
        self.close()

    def chunk(self):
        """
        Should return a block of uint numpy arrays
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
        Returns a numpy array of uints otherwise
        """

        # Calculate remainin unread bytes
        difference = self.filesize - self._f.tell()

        # Read a complete symbol of uints
        if difference > self.symbolsize:
            return numpy.fromfile(self._f, dtype=self.dtype, count=self.ints_to_read)

        # Read the remainder
        elif difference > 0:
            return self._f.read()

        return None

    def get_block_id(self):
        """
        Gets the current block id and increments to prepare for the next block.
        Returns the current block id
        """
        r = self.block_id
        self.block_id += 1
        return r

    def close(self):
        """
        Attempts to close the file associated with this chunker
        """
        try:
            self._f.close()
        except:
            pass
