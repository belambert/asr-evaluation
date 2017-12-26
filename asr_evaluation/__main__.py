#!/usr/bin/env python

# Copyright 2017-2018 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains the main method for the CLI.
"""

import argparse

# For some reason Python 2 and Python 3 disagree about how to import this.
try:
    from asr_evaluation.asr_evaluation import main as other_main
except Exception:
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
    parser.add_argument('--head-ids', action='store_true',
                        help='Hypothesis and reference files have ids in the first token? (Kaldi format)')
    parser.add_argument('-id', '--tail-ids', '--has-ids', action='store_true',
                        help='Hypothesis and reference files have ids in the last token? (Sphinx format)')
    parser.add_argument('-c', '--confusions', action='store_true', help='Print tables of which words were confused.')
    parser.add_argument('-p', '--print-wer-vs-length', action='store_true',
                        help='Print table of average WER grouped by reference sentence length.')
    parser.add_argument('-m', '--min-word-count', type=int, default=1, metavar='count',
                        help='Minimum word count to show a word in confusions (default 1).')
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
