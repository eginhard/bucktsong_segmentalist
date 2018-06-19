#!/usr/bin/env python

"""
Cut segments from a .npz file using a "label_utterance_start-end" convention.

Author: Herman Kamper
Contact: h.kamper@sms.ed.ac.uk
Date: 2015
"""

import argparse
import mmap
import numpy as np
import sys
from tqdm import tqdm
from copy import deepcopy


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("input_npz_fn", type=str, help="")
    parser.add_argument("segments_fn", type=str, help="")
    parser.add_argument("output_npz_fn", type=str, help="")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    output_npz = {}
    total_target_segs = 0
    with open(args.segments_fn) as f, np.load(args.input_npz_fn) as input_npz:
      for line in tqdm(f, total=get_num_lines(args.segments_fn)):
        total_target_segs += 1
        line_split = line.strip().split("###")
        utterance = line_split[1]
        start = int(line_split[2])
        end = int(line_split[3])
        target_seg_key = line.strip()
        if utterance in input_npz:
            output_npz[target_seg_key] = deepcopy(input_npz[utterance][start:end])
        else:
            print "Missed:", target_seg_key

    print "Extracting target segments"

    print "Extracted " + str(len(output_npz.keys())) + " out of " + str(total_target_segs) + " segments"
    print "Writing:", args.output_npz_fn
    np.savez(args.output_npz_fn, **output_npz)


if __name__ == "__main__":
    main()

