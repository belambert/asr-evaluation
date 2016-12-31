#!/usr/bin/env python

import argparse
from asr_evaluation import main as other_main

def get_parser():
    parser = argparse.ArgumentParser(description='Evaluate an ASR transcript against a reference transcript.')
    parser.add_argument('ref', type=argparse.FileType('r'), help='Reference transcript filename')
    parser.add_argument('hyp', type=argparse.FileType('r'), help='ASR hypothesis filename')
    parser.add_argument('-i', '--print-instances', action='store_true',
                        help='Print the individual sentences and their errors')
    parser.add_argument('-id', '--has-ids', action='store_true',
                        help='Hypothesis and reference files have ids in the last token?')
    parser.add_argument('-c', '--confusions', action='store_true', help='Print tables of which words were confused')
    parser.add_argument('-p', '--print-wer-vs-length', action='store_true',
                        help='Print table of average WER grouped by reference sentence length')
    parser.add_argument('-m', '--min-word-count', type=int, default=10, metavar='count',
                        help='Minimum word count to show a word in confusions')
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    other_main(args)

if __name__ == "__main__":
    main()
