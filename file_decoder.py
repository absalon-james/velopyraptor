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
from decoder import Decoder
from bitarray import bitarray

class FileDecoder(object):

    """
    Decodes a RaptorR10 encoded directory into
    the original file
    """

    def __init__(self, input_dir, output_file):
        """
        Initializes an instance of FileDecoder

        Arguments:
        input_dir   -- Directory containing blocks and shares to decode
        output_file -- Target file to assemble decoded blocks into
        """
        self.input_dir = input_dir
        self.output_file = output_file
        self.stats = {
            'io_time': 0,
            'decoding_time': 0
        }

    def start_timer(self):
        """
        Dumbed down timer. Grab a new timestamp
        """
        self.t = time.time()

    def stop_timer(self):
        """
        Dumbed down timer.  Returns a float difference in seconds
        between now and a previous time
        """
        delta = time.time() - self.t
        self.t = None
        return delta

    def add_time(self, delta, field):
        """
        Convience function for adding a time delta to one
        of the time tracking stats.

        Arguments:
        delta -- Float difference in seconds
        field -- Key to add to within the stats dict
        """
        self.stats[field] += delta

    def exit(self, message):
        """
        Prints a simple message and then exits

        Arguments:
        message -- String message to print prior to exiting
        """
        print message
        exit()

    def verify_input_dir(self):
        """
        Verifies that the input directory exists and is a directory
        """
        if not os.path.exists(self.input_dir):
            self.exit("Directory '%s' doesn't exist." % self.input_dir)

        if not os.path.isdir(self.input_dir):
            self.exit("%s isn't a directory." % self.input_dir)

    def verify_output_file(self):
        """
        Verifies that the output file does not already exist
        """
        if os.path.exists(self.output_file):
            self.exit("File %s already exists." % self.output_file)

    def read_block_meta_data(self, blockdir):
        """
        Reads a metadata file to obtain padding and coding parameters

        Arguments:
        blockdir -- String of the block directory

        Returns:
        a tuple with (integer k, integer padding(Bytes))
        """
        metafile = os.path.join(blockdir, 'meta')
        try:
            f = open(metafile, 'r')
            line = f.readline()
            f.close()
            k, padding = line.split(':')
            return (int(k), int(padding))
        except:
            self.exit("Unable to read block metadata for block %s." % metafile)
            

    def decode(self):
        """
        Orchestrates the reading of file shares into encoded symbols
        and decoding of the encoded symbols
        """
        self.stats['start_time'] = time.time()

        self.verify_input_dir()
        self.verify_output_file()

        # Outer loop will iterate over blocks in a directory.
        # Block directories contain shares per block.
        # Blocks start at 0 and increment by 1.  If block n doesn't exist
        # Then assume that is the end of the file
        block = 0
        blockdir = os.path.join(self.input_dir, str(block))
        while os.path.exists(blockdir):

            print "Decoding block %s" % blockdir

            # Attempt to read metadata for this block
            self.start_timer()
            k, padding = self.read_block_meta_data(blockdir)
            self.add_time(self.stop_timer(), 'io_time')

            # For each file in the block directory(excluding meta) read each
            # share.  Each will be an encoding symbol

            decoder = Decoder(k)
            read_symbols = 0

            for _file in os.listdir(blockdir):
                
                # Skip non files
                if not os.path.isfile(os.path.join(blockdir, _file)):
                    continue

                try:
                    # A share should be a named integer indicating which symbol it
                    # is.  int(_file) will raise an error if not and we ignore
                    # that file
                    id = int(_file)

                    # Open the share file in binary mode
                    self.start_timer()
                    f = io.open(os.path.join(blockdir, _file), 'r+b')
                    ba = bitarray()
                    ba.frombytes(f.read())
                    f.close()
                    self.add_time(self.stop_timer(), 'decoding_time')

                    # Add the symbol to the decoder.
                    # A symbol is a (integer, bitarray) tuple
                    decoder.append((int(_file), ba))
                    read_symbols += 1
                except Exception, e:
                    continue
                    pass

            # Ideally we want more than k encoded symbols.
            # We will fail with less than k
            if read_symbols < k:
                self.exit("There were not sufficient symbols to recover block %s" % block)

            # Instruct decoder to calculate intermediate symbols from
            # known encoding symbols
            self.start_timer()
            decoder.decode()
            self.add_time(self.stop_timer(), 'decoding_time')

            # Steam source symbol output by encoding the first
            # k encoded symbols.
            # The first k source symbols == the first k encoding symbols
            target = io.open(self.output_file, 'a+b')
            for i in xrange(k):

                self.start_timer()
                s = decoder.next()[1].tobytes()
                self.add_time(self.stop_timer(), 'decoding_time')

                self.start_timer()
                target.write(s)
                self.add_time(self.stop_timer(), 'io_time')
            target.close()
        
            # Padding should only be on the last block but we check anyway
            # @TODO - Ensure file size is accurate before truncating
            if (padding):
                self.start_timer()
                size = os.path.getsize(self.output_file) - padding
                target = io.open(args.file, 'a+b')
                target.truncate(size)
                target.close()
                self.add_time(self.stop_timer(), 'io_time')
    
            # Increment block number by 1
            block += 1
            blockdir = os.path.join(self.input_dir, str(block))

        self.stats['blocks_decoded'] = block
        self.stats['end_time'] = time.time()
        self.stats['elapsed_time'] = self.stats['end_time'] - self.stats['start_time']

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="python file_decoder.py", description="Erasure decoding using Raptor R10")
    parser.add_argument('directory', help="Directory to decode")
    parser.add_argument('file', help="Output file")
    args = parser.parse_args()
    decoder = FileDecoder(args.directory, args.file)
    decoder.decode()

    print "Finished decoding directory %s into %s" % (args.directory, args.file)
    print "Elapsed time: %s seconds" % (decoder.stats['elapsed_time'])
    print "Io time: %s seconds" % (decoder.stats['io_time'])
    print "Decoding time: %s seconds" % (decoder.stats['decoding_time'])
