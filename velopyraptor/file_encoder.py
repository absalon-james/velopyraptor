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

import os
import io
import time
from encoder import Encoder
from chunker import FileChunker

class FileEncoder(object):

    """
    Given the number of source symbols and symbol size, an instance
    of this class will encode a block of the source at a time writing
    out the shares
    """

    def __init__(self, k, s, m, input_file, output_dir):
        """
        Initializes an instance of a file encoder

        Arguments
        k          -- Integer number of source symbols
        s          -- Integer symbolsize in Bytes
        m          -- Intger number of parity symbols
        input_file -- File to encode
        output_dir -- Directory to place encoded blocks and shares
        """
        self.k = k
        self.s = s # Bytes
        self.m = m
        self.input_file = input_file
        self.output_dir = output_dir
        self.stats = {
            'chunking_time': 0,
            'encoding_time': 0
        }
        self.t = None

    def start_timer(self):
        """
        Dumbed down timer.  Grab a timestamp
        """
        self.t = time.time()

    def stop_timer(self):
        """
        Dumbed down timer.  Grab a new time stamp
        and return the difference

        Returns a float number of seconds between now and the start time
        """
        delta = time.time() - self.t
        self.t = None
        return delta

    def add_time(self, delta, field):
        """
        Convenience function for adding cumulative time to
        time measurements in stats

        Arguments:
        delta -- Float number of seconds between two times
        field -- String field to add the delta to
        """
        self.stats[field] += delta 

    def exit(self, message):
        """
        Exits after printing a message


        Arguments:
        message -- String to print prior to exiting
        """
        print message
        exit()

    def make_output_dir(self):
        """
        Ensures target directory does not exist before making it
        """
        # Check output directory - die if it exists
        if os.path.exists(self.output_dir):
            self.exit("Directory '%s' already exists." % self.output_dir)

        # Make the directory
        try:
            os.makedirs(args.directory)
        except:
            self.exit("Unable to create directory %s." % self.output_dir)

    def encode(self):
        """
        Creates a file chunker and iterates over each chunk decoding a chunk
        at a time to reduce memory costs
        """

        self.stats['start_time'] = time.time()

        self.start_timer()

        with FileChunker(self.k, self.s, self.input_file) as chunker:
            self.add_time(self.stop_timer(), 'chunking_time')
            block_name = 0

            # Chunker returns none when we are out of blocks
            self.start_timer()
            block = chunker.chunk()
            self.add_time(self.stop_timer(), 'chunking_time')
            while(block):

                # Create the block directory
                dir_name = os.path.join(self.output_dir, str(block_name))
                os.makedirs(dir_name)

                # The k source symbols are the first k encoding symbols
                # The id is used to calculate a triple
                source_symbols = [(id, block[id]) for id in xrange(self.k)]

                self.start_timer()
                encoder = Encoder(self.k, source_symbols)
                self.add_time(self.stop_timer(), 'encoding_time')

                # Write padding and k parameters that will be used
                # to decode the block
                # @TODO - Pack integers into bytes and write to binary file
                #   Instead of text
                f = open(os.path.join(dir_name, 'meta'), 'w')
                f.write("%s:%s" % (block.k, block.padding))
                f.close()

                # Iterate over the encoder and produce the first k + m symbols
                # In this instance the first k symbols will match the source symbols
                # m is the number of parity blocks
                # NOTE - We could start at k and produce k+m symbols there consisting
                # entirely of parity blocks and be just as fine
                for i in xrange(self.k + self.m):

                    # Each share will be named its id (share 0 is named 0)

                    # The encoder produces an (id, numpy array) tuple
                    self.start_timer()
                    sid, symbol = encoder.next()
                    self.add_time(self.stop_timer(), 'encoding_time')
                    symbol.tofile(os.path.join(dir_name, str(i)))
                    f.close()

                block_name += 1
                self.start_timer()
                block = chunker.chunk()
                self.add_time(self.stop_timer(), 'chunking_time')

        self.stats['blocksize'] = self.k * self.s
        self.stats['symbolsize'] = self.s
        self.stats['num_blocks'] = block_name
        self.stats['end_time'] = time.time()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog="python file_encoder.py",
        description="Erasure encoding using raptor r10"
    )

    parser.add_argument('file', help="File to encode")
    parser.add_argument(
        'directory',
        help="Output directory to contain encoded shares"
    )

    parser.add_argument("--k", default=10, type=int, help="Number of nodes to split encoding.(default 10)")
    parser.add_argument('--m', default=4, type=int, help="Number of parity blocks to compute.(default 4)")
    parser.add_argument('--s', default=(1 * 1024 * 1024), type=int, help="Symbol size in bytes(default 1 * 1024 * 1024)")

    args = parser.parse_args()
    encoder = FileEncoder(args.k, args.s, args.m, args.file, args.directory)
    encoder.encode()

    print "Finished encoding %s into directory %s" % (args.file, args.directory)
    print "\nTotal Time: %s s" % (encoder.stats['end_time'] - encoder.stats['start_time'])
    print "Chunking Time: %s s" % (encoder.stats['chunking_time'])
    print "Encoding Time: %s s" % (encoder.stats['encoding_time'])

    print "\nBlocksize: %s Bytes" % (encoder.stats['blocksize'])
    print "Symbolsize: %s Bytes" % (encoder.stats['symbolsize'])
    print "Number Blocks: %s" % (encoder.stats['num_blocks'])
