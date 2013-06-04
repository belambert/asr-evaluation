from __future__ import division

import editdistance
import sys
import argparse
import numpy
from itertools import izip
from collections import defaultdict

# This is the command line interface!
parser = argparse.ArgumentParser(description='Evaluate an ASR transcript against a reference transcript.')
parser.add_argument('ref', type=file, help='the reference transcript filename')
parser.add_argument('hyp', type=file, help='the ASR hypothesis filename')
parser.add_argument('-i', '--print-instances', action='store_true', help='print the individual sentences and their errors')
parser.add_argument('-id', '--has-ids', action='store_true', help='hypothesis and reference files have ids in the last token?')
parser.add_argument('-c', '--confusions', action='store_true', help='print tables of which words were confused')
parser.add_argument('-p', '--plot-wer-vs-length', action='store_true', help='print tables of which words were confused')
parser.add_argument('-m', '--min-word-count', type=int, default=10, metavar='count', help='minimum word count to show a word in confusions')
args = parser.parse_args()

print_instances = args.print_instances
files_have_ids = args.has_ids
confusions = args.confusions
min_count= args.min_word_count
plot= args.plot_wer_vs_length

ref_token_count = 0
error_count = 0
match_count = 0

lengths = []
error_rates = []
wer_bins = [[] for x in xrange(20)]

def main():
    global error_count
    global match_count
    global ref_token_count

    counter = 1
    for ref_line, hyp_line in izip(args.ref, args.hyp):
        ref = ref_line.split()
        hyp = hyp_line.split()
        id = None
        if files_have_ids:
            ref_id = ref[-1]
            hyp_id = hyp[-1]
            assert (ref_id == hyp_id)
            id = ref_id
            ref = ref[:-1]
            hyp = hyp[:-1]
            #sm = editdistance.SequenceMatcher(a=ref, b=hyp, action_function=editdistance.highest_match_action)
            sm = editdistance.SequenceMatcher(a=ref, b=hyp)
        errors = get_error_count(sm)
        matches = get_match_count(sm)
        ref_length = len(ref)
        error_count += errors
        match_count += matches
        ref_token_count += ref_length
        
        if confusions:
            track_confusions(sm, ref, hyp)
        if print_instances:
            print_diff(sm, ref, hyp)
            if id:
                print "SENTENCE %d  %s"%(counter, id)
            else:
                print "SENTENCE %d"%counter
            print "Correct          = %5.1f%%  %3d   (%6d)" % (100.0 * matches / ref_length, matches, match_count)
            print "Errors           = %5.1f%%  %3d   (%6d)" % (100.0 * errors / ref_length, errors, error_count)
        lengths.append(ref_length)
        error_rates.append(errors * 1.0 / len(ref))
        wer_bins[len(ref)].append(errors * 1.0 / len(ref))
        counter = counter + 1
    if confusions:
        print_confusions()
    if plot:
        plot_wers()

    wers_vs_length()
    print "WRR: %f %% (%10d / %10d)"%(100*match_count/ref_token_count, match_count, ref_token_count)
    print "WER: %f %% (%10d / %10d)"%(100*error_count/ref_token_count, error_count, ref_token_count)


insertion_table = defaultdict(int)
deletion_table = defaultdict(int)
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

# For some reason I'm getting two different counts depending on how I count the matches....
def get_match_count(sm):
    "Return the number of matches, given a sequence matcher object."
    matches = None
    # try:
    #     matches = sm.matches()
    # except:
    matching_blocks = sm.get_matching_blocks()
    matches = reduce(lambda x, y: x + y, map(lambda x: x[2], matching_blocks), 0)
    return matches

error_codes = ['replace', 'delete', 'insert']

def get_error_count(sm):
    """Return the number of errors (insertion, deletion, and substitutiions
    , given a sequence matcher object."""
    opcodes = sm.get_opcodes()
    errors = filter(lambda x: x[0] in error_codes, opcodes)
    error_lengths = map(lambda x: max (x[2] - x[1], x[4] - x[3]), errors)
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
    print "REF: %s"%' '.join(ref_tokens)
    print "HYP: %s"%' '.join(hyp_tokens)



def wers_vs_length():
    avg_wers = map(numpy.mean, wer_bins)
    for i in range(len(avg_wers)):
        print "%5d %f"%(i, avg_wers[i])
    print ""

    
# import matplotlib
# #import pylab
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.mlab as mlab
# import numpy

# def plot_wers():
#         # Create a figure with size 6 x 6 inches.
#     fig = Figure(figsize=(6,6))
#     # Create a canvas and add the figure to it.
#     canvas = FigureCanvas(fig)
#     # Create a subplot.
#     ax = fig.add_subplot(111)
#     # Set the title.
#     ax.set_title("WER vs sentence length",fontsize=14)
#     # Set the X Axis label.
#     ax.set_xlabel("sentence length (# of words)",fontsize=12)    
#     # Set the Y Axis label.
#     ax.set_ylabel("WER", fontsize=12)
#     # Display Grid.
#     #ax.grid(True,linestyle='-',color='0.75')    
#     # Generate the Scatter Plot.
#     #ax.scatter(lengths, error_rates, s=20,color='tomato');    
#     ax.scatter(lengths, error_rates, color='tomato');    
#     # Save the generated Scatter Plot to a PNG file.
#     canvas.print_figure('wer-vs-length.png',dpi=500)



if __name__ == "__main__":
    main()
