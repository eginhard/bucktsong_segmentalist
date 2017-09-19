#!/usr/bin/env python

"""
Cut segments from a .npz file using a "label_utterance_start-end" convention.

Author: Herman Kamper
Contact: h.kamper@sms.ed.ac.uk
Date: 2015
"""

import argparse
import numpy as np
import sys


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


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    # Read the .npz file
    print "Reading npz:", args.input_npz_fn
    input_npz = np.load(args.input_npz_fn)

    # Create target segments dict
    print "Reading segments:", args.segments_fn
    target_segs = {}  # target_segs["years SP008_1 4951 5017"] is ("SP008_1", 4951, 5017)
    for line in open(args.segments_fn):
        line_split = line.strip().split("###")
        utterance = line_split[1]
        start = int(line_split[2])
        end = int(line_split[3])
        target_segs[line.strip()] = (utterance, start, end)

    print "Extracting target segments"
    output_npz = {}
    n_target_segs = 0
    for target_seg_key in target_segs:
        utterance, start, end = target_segs[target_seg_key]

        if utterance in input_npz:
            output_npz[target_seg_key] = input_npz[utterance][start:end]
            n_target_segs += 1

        if not target_seg_key in output_npz:
            print "Missed:", target_seg_key

    print "Extracted " + str(n_target_segs) + " out of " + str(len(target_segs)) + " segments"
    print "Writing:", args.output_npz_fn
    np.savez(args.output_npz_fn, **output_npz)


if __name__ == "__main__":
    main()

