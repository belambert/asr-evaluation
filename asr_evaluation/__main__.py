#!/usr/bin/env python
"""
Contains the main method for the CLI.
"""

import argparse

# For some reason Python 2 and Python 3 disagree about how to import this.
try:
    from asr_evaluation.asr_evaluation import main as other_main
except:
    from asr_evaluation import main as other_main

def get_parser():
    """Parse the CLI args."""
    parser = argparse.ArgumentParser(description='Evaluate an ASR transcript against a reference transcript.')
    parser.add_argument('ref', type=argparse.FileType('r'), help='Reference transcript filename')
    parser.add_argument('hyp', type=argparse.FileType('r'), help='ASR hypothesis filename')
    print_args = parser.add_mutually_exclusive_group()
    print_args.add_argument('-i', '--print-instances', action='store_true',
                            help='Print all individual sentences and their errors.')
    print_args.add_argument('-r', '--print-errors', action='store_true',
                            help='Print all individual sentences that contain errors.')
    parser.add_argument('-id', '--has-ids', action='store_true',
                        help='Hypothesis and reference files have ids in the last token?')
    parser.add_argument('-c', '--confusions', action='store_true', help='Print tables of which words were confused.')
    parser.add_argument('-p', '--print-wer-vs-length', action='store_true',
                        help='Print table of average WER grouped by reference sentence length.')
    parser.add_argument('-m', '--min-word-count', type=int, default=10, metavar='count',
                        help='Minimum word count to show a word in confusions.')
    parser.add_argument('-a', '--case-insensitive', action='store_true',
                        help='Down-case the text before running the evaluation.')
    parser.add_argument('-e', '--remove-empty-refs', action='store_true',
                        help='Skip over any examples where the reference is empty.')

    return parser

def main():
    """Run the program."""
    parser = get_parser()
    args = parser.parse_args()
    other_main(args)

if __name__ == "__main__":
    main()
