

import argparse
# import asr_evaluation
from asr_evaluation.asr_evaluation import main as other_main

def get_parser():
    parser = argparse.ArgumentParser(description='Evaluate an ASR transcript against a reference transcript.')
    # parser.add_argument('ref', type=file, help='the reference transcript filename')
    # parser.add_argument('hyp', type=file, help='the ASR hypothesis filename')
    parser.add_argument('ref', help='the reference transcript filename')
    parser.add_argument('hyp', help='the ASR hypothesis filename')
    parser.add_argument('-i', '--print-instances', action='store_true', help='print the individual sentences and their errors')
    parser.add_argument('-id', '--has-ids', action='store_true', help='hypothesis and reference files have ids in the last token?')
    parser.add_argument('-c', '--confusions', action='store_true', help='print tables of which words were confused')
    parser.add_argument('-p', '--print-wer-vs-length', action='store_true', help='print table of average WER grouped by reference sentence length')
    parser.add_argument('-m', '--min-word-count', type=int, default=10, metavar='count', help='minimum word count to show a word in confusions')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    # print(dir(asr_evaluation))
    other_main(args)
    
if __name__ == "__main__":
    main()



