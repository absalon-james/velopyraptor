import argparse
import cProfile
import os
import pstats
import shutil
from file_encoder import FileEncoder

profile_results_name = "profile_results"

parser = argparse.ArgumentParser(
    prog="python profile.py",
    description="Profiling of file encoder"
)

parser.add_argument('file', help="File to encode")
parser.add_argument('directory', help="Output directory")

parser.add_argument("--k", type=int, default=10, help="Number of source symbols")
parser.add_argument("--m", type=int, default=4, help="Number of parity symbols")
parser.add_argument("--s", type=int, default=1048576, help="Symbol size in bytes")
parser.add_argument("--o", default=False, action="store_true", help="Use optimal symbols when encoding")
parser.add_argument("--clean", default=False, action="store_true", help="Clean up after self")

args = parser.parse_args()
encoder = FileEncoder(args.k, args.s, args.m, args.file, args.directory, optimal=args.o)

cProfile.run("encoder.encode()", profile_results_name)
stats = pstats.Stats(profile_results_name)
stats.sort_stats("cumulative").print_stats(20)

if args.clean:
    os.remove(profile_results_name)
    shutil.rmtree(args.directory)
