from __future__ import division

import difflib
import sys
import argparse
from itertools import izip
from collections import defaultdict

# This is the command line interface!
parser = argparse.ArgumentParser(description='Evaluate an ASR transcript against a reference transcript.')
parser.add_argument('ref', type=file, help='the reference transcript filename')
parser.add_argument('hyp', type=file, help='the ASR hypothesis filename')
parser.add_argument('-i', '--print-instances', action='store_true', help='print the individual sentences and their errors')
parser.add_argument('-id', '--has-ids', action='store_true', help='hypothesis and reference files have ids in the last token?')
parser.add_argument('-c', '--confusions', action='store_true', help='print tables of which words were confused')

parser.add_argument('-m', '--min-word-count', type=int, default=10, metavar='count', help='minimum word count to show a word in confusions')

args = parser.parse_args()

print_instances = args.print_instances
files_have_ids = args.has_ids
confusions = args.confusions
min_count= args.min_word_count

ref_token_count = 0
error_count = 0
match_count = 0

def main():
    global error_count
    global match_count
    global ref_token_count

    for ref_line, hyp_line in izip(args.ref, args.hyp):
        ref = ref_line.split()
        hyp = hyp_line.split()

        if files_have_ids:
            ref = ref[:-1]
            hyp = hyp[:-1]
        sm = difflib.SequenceMatcher(a=ref, b=hyp)
        errors = get_error_count(sm)
        matches = get_match_count(sm)
        error_count += errors
        match_count += matches
        ref_token_count += len(ref)
        if confusions:
            track_confusions(sm, ref, hyp)
        if print_instances:
            print_diff(sm, ref, hyp)

    if confusions:
        print_confusions()
    

    print "WRR: %f %% (%10d / %10d)"%(100*match_count/ref_token_count, match_count, ref_token_count)
    print "WER: %f %% (%10d / %10d)"%(100*error_count/ref_token_count, error_count, ref_token_count)


insertion_table = defaultdict(int)
deletion_table = defaultdict(int)
#substituion_table = defaultdict(defaultdict(int))
substitution_table = defaultdict(int)

def print_confusions ():
    if len(insertion_table) > 0:
        print "INSERTIONS:"
        for item in sorted(insertion_table.items(), key=lambda x: x[1], reverse=True):
            if item[1] > min_count:
                print "%20s %10d"%item
    if len(deletion_table) > 0:
        print "DELETIONS:"
        for item in sorted(deletion_table.items(), key=lambda x: x[1], reverse=True):
            if item[1] > min_count:
                print "%20s %10d"%item    
    if len(substitution_table) > 0:
        print "SUBSTITUTIONS:"
        for [w1, w2], count in sorted(substitution_table.items(), key=lambda x: x[1], reverse=True):
            if count > min_count:
                print "%20s -> %20s   %10d"%(w1, w2, count)

def track_confusions(sm, seq1, seq2):
    "Keep track of the errors in a global variable, given a sequence matcher."
    opcodes = sm.get_opcodes()
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'insert':
            for i in range(j1,j2):
                word = seq2[i]
                insertion_table[word] += 1
        elif tag == 'delete':
            for i in range(i1,i2):
                word = seq1[i]
                deletion_table[word] += 1
        elif tag == 'replace':
            for w1 in seq1[i1:i2]:
                for w2 in seq2[j1:j2]:
                    key = (w1, w2)
                    substitution_table[key] += 1

def get_match_count(sm):
    "Return the number of matches, given a sequence matcher object."
    matches = sm.get_matching_blocks()
    return reduce(lambda x, y: x + y, map(lambda x: x[2], matches), 0)

error_codes = ['replace', 'delete', 'insert']

def get_error_count(sm):
    """Return the number of errors (insertion, deletion, and substitutiions
    , given a sequence matcher object."""
    opcodes = sm.get_opcodes()
    errors = filter(lambda x: x[0] in error_codes, opcodes)
    error_lengths = map(lambda x: x[4] - x[3], errors)
    return reduce(lambda x, y: x + y, error_lengths, 0)
    
def print_diff(sm, seq1, seq2):
    """Given a sequence matcher and the two sequences, print a Sphinx-style
    'diff' off the two."""
    ref_tokens = []
    hyp_tokens = []
    opcodes = sm.get_opcodes()
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            for i in range(i1,i2):
                ref_tokens.append(seq1[i].lower())
            for i in range(j1,j2):
                hyp_tokens.append(seq2[i].lower())
        elif tag == 'delete':
            for i in range(i1,i2):
                ref_tokens.append(seq1[i].upper())
            for i in range(i1,i2):
                hyp_tokens.append('*' * len(seq1[i]))
        elif tag == 'insert':
            for i in range(j1,j2):
                ref_tokens.append('*' * len(seq2[i]))
            for i in range(j1,j2):
                hyp_tokens.append(seq2[i].upper())
        elif tag == 'replace':
            seq1_len = i2 - i1
            seq2_len = j2 - j1
            s1 = map(str.upper, seq1[i1:i2])
            s2 = map(str.upper, seq2[j1:j2])
            if seq1_len > seq2_len:
                for i in range(0, seq1_len-seq2_len):
                    s2.append(False)
            if seq1_len < seq2_len:
                for i in range(0, seq2_len-seq1_len):
                    s1.append(False)
            assert(len(s1) == len(s2))
            for i in range(0,len(s1)):
                w1 = s1[i]
                w2 = s2[i]
                # If we have two words, make them the same length
                if w1 and w2:
                    if len(w1) > len(w2):
                        s2[i] = w2 + ' '*(len(w1) - len(w2))
                    elif len(w1) < len(w2):
                        s1[i] = w1 + ' '*(len(w2) - len(w1))
                # Otherwise, create an empty word of the right width
                if w1 == False:
                    s1[i] = '*'*len(w2)
                if w2 == False:
                    s2[i] = '*'*len(w1)
            ref_tokens += s1
            hyp_tokens += s2

    print '='*60
    print ' '.join(ref_tokens)
    print ' '.join(hyp_tokens)




if __name__ == "__main__":
    main()
