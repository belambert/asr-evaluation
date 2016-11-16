
from functools import reduce
from collections import defaultdict
from edit_distance import SequenceMatcher

from termcolor import colored

# Imports for plotting
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# For keeping track of the total number of tokens, errors, and matches
ref_token_count = 0
error_count = 0
match_count = 0

# For keeping track of word error rates by sentence length
# this is so we can see if performance is better/worse for longer
# and/or shorter sentences
lengths = []
error_rates = []
wer_bins = defaultdict(list)
wer_vs_length = defaultdict(list)
# Tables for keeping track of which words get confused with one another
insertion_table = defaultdict(int)
deletion_table = defaultdict(int)
substitution_table = defaultdict(int)
# These are the editdistance opcodes that are condsidered 'errors'
error_codes = ['replace', 'delete', 'insert']


# TODO - rename this function.  Move some of it into evaluate.py?
def main(args):
    """Main method - this reads the hyp and ref files, and creates
    editdistance.SequenceMatcher objects to compute the edit distance.
    All the statistics necessary statistics are collected, and results are
    printed as specified by the command line options.

    This function doesn't not check to ensure that the reference and
    hypothesis file have the same number of lines.  It will stop after the
    shortest one runs out of lines.  This should be easy to fix...
    """
    global error_count
    global match_count
    global ref_token_count
    global confusions
    set_global_variables(args)

    counter = 1
    # Loop through each line of the reference and hyp file
    for ref_line, hyp_line in zip(args.ref, args.hyp):
        process_line_pair(ref_line, hyp_line)
        counter += 1
    if confusions:
        print_confusions()
    if wer_vs_length:
        print_wer_vs_length()
    print('WRR: {0:f} % ({1:10d} / {2:10d})'.format(100 * match_count / ref_token_count, match_count, ref_token_count))
    print('WER: {0:f} % ({1:10d} / {2:10d})'.format(100 * error_count / ref_token_count, error_count, ref_token_count))


def process_line_pair(ref_line, hyp_line):
    """Given a pair of strings corresponding to a reference and hypothesis,
    compute the edit distance, print if desired, and keep track of results
    in global variables."""
    # I don't believe these all need to be global.  In any case, they shouldn't be.
    global error_count
    global match_count
    global ref_token_count
    global print_instances
    global files_have_ids
    global confusions
    global min_count
    global plot

    ref = ref_line.split()
    hyp = hyp_line.split()
    id_ = None

    # If the files have IDs, then split the ID off from the text
    if files_have_ids:
        remove_sentence_ids(ref, hyp)

    # Create an object to get the edit distance, and then retrieve the
    # relevant counts that we need.
    sm = SequenceMatcher(a=ref, b=hyp)
    errors = get_error_count(sm)
    matches = get_match_count(sm)
    ref_length = len(ref)

    # Increment the total counts we're tracking
    error_count += errors
    match_count += matches
    ref_token_count += ref_length

    # If we're keeping track of which words get mixed up with which others, call track_confusions
    if confusions:
        track_confusions(sm, ref, hyp)

    # If we're printing instances, do it here (in roughly the align.c format)
    if print_instances:
        print_instances(ref, hyp, sm, id_=id_)

    # Keep track of the individual error rates, and reference lengths, so we
    # can compute average WERs by sentence length
    lengths.append(ref_length)
    if len(ref) > 0:
        error_rate = errors * 1.0 / len(ref)
    else:
        error_rate = float("inf")
    error_rates.append(error_rate)
    wer_bins[len(ref)].append(error_rate)

def set_global_variables(args):
    global print_instances
    global files_have_ids
    global confusions
    global min_count
    global plot
    # Put the command line options into global variables.
    print_instances = args.print_instances
    files_have_ids = args.has_ids
    confusions = args.confusions
    min_count = args.min_word_count
    plot = args.print_wer_vs_length

def remove_sentence_ids(ref, hyp):
    """Assumes that the ID is the final token of the string which is common
    in Sphinx but not in Kaldi."""
    ref_id = ref[-1]
    hyp_id = hyp[-1]
    assert (ref_id == hyp_id)
    ref = ref[:-1]
    hyp = hyp[:-1]
    return ref, hyp

def print_instances(ref, hyp, sm, id_=None):
    print_diff(sm, ref, hyp)
    if id_:
        print(('SENTENCE {0:d}  {1!s}'.format(counter, id_)))
    else:
        print('SENTENCE {0:d}'.format(counter))
    print('Correct          = {0:5.1f}%  {1:3d}   ({2:6d})'.format(100.0 * matches / ref_length, matches, match_count))
    print('Errors           = {0:5.1f}%  {1:3d}   ({2:6d})'.format(100.0 * errors / ref_length, errors, error_count))

def track_confusions(sm, seq1, seq2):
    """Keep track of the errors in a global variable, given a sequence matcher."""
    opcodes = sm.get_opcodes()
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'insert':
            for i in range(j1, j2):
                word = seq2[i]
                insertion_table[word] += 1
        elif tag == 'delete':
            for i in range(i1, i2):
                word = seq1[i]
                deletion_table[word] += 1
        elif tag == 'replace':
            for w1 in seq1[i1:i2]:
                for w2 in seq2[j1:j2]:
                    key = (w1, w2)
                    substitution_table[key] += 1

def print_confusions():
    """Print the confused words that we found... grouped by insertions, deletions
    and substitutions."""
    if len(insertion_table) > 0:
        print('INSERTIONS:')
        for item in sorted(list(insertion_table.items()), key=lambda x: x[1], reverse=True):
            if item[1] > min_count:
                print('{0:20!s} {1:10d}'.format(*item))
    if len(deletion_table) > 0:
        print('DELETIONS:')
        for item in sorted(list(deletion_table.items()), key=lambda x: x[1], reverse=True):
            if item[1] > min_count:
                print('{0:20!s} {1:10d}'.format(*item))
    if len(substitution_table) > 0:
        print('SUBSTITUTIONS:')
        for [w1, w2], count in sorted(list(substitution_table.items()), key=lambda x: x[1], reverse=True):
            if count > min_count:
                print('{0:20!s} -> {1:20!s}   {2:10d}'.format(w1, w2, count))

# For some reason I was getting two different counts depending on how I count the matches,
# so do an assertion in this code to make sure we're getting matching counts.
# This might slow things down?
def get_match_count(sm):
    "Return the number of matches, given a sequence matcher object."
    matches = None
    matches1 = sm.matches()
    matching_blocks = sm.get_matching_blocks()
    matches2 = reduce(lambda x, y: x + y, [x[2] for x in matching_blocks], 0)
    assert(matches1 == matches2)
    matches = matches1
    return matches


def get_error_count(sm):
    """Return the number of errors (insertion, deletion, and substitutiions
    , given a sequence matcher object."""
    opcodes = sm.get_opcodes()
    errors = [x for x in opcodes if x[0] in error_codes]
    error_lengths = [max(x[2] - x[1], x[4] - x[3]) for x in errors]
    return reduce(lambda x, y: x + y, error_lengths, 0)

# This is long and ugly.  Perhaps we can break it up?
# It would make more sense for this to just return the two strings...
def print_diff(sm, seq1, seq2, prefix1='REF:', prefix2='HYP:', suffix1=None, suffix2=None):
    """Given a sequence matcher and the two sequences, print a Sphinx-style
    'diff' off the two."""
    ref_tokens = []
    hyp_tokens = []
    opcodes = sm.get_opcodes()
    for tag, i1, i2, j1, j2 in opcodes:
        # If they are equal, do nothing except lowercase them
        if tag == 'equal':
            for i in range(i1, i2):
                ref_tokens.append(seq1[i].lower())
            for i in range(j1, j2):
                hyp_tokens.append(seq2[i].lower())
        # For insertions and deletions, put a filler of '***' on the other one, and
        # make the other all caps
        elif tag == 'delete':
            for i in range(i1, i2):
                ref_token = colored(seq1[i].upper(), 'red')
                ref_tokens.append(ref_token)
            for i in range(i1, i2):
                hyp_token = colored('*' * len(seq1[i]), 'red')
                hyp_tokens.append(hyp_token)
        elif tag == 'insert':
            for i in range(j1, j2):
                ref_token = colored('*' * len(seq2[i]), 'red')
                ref_tokens.append(ref_token)
            for i in range(j1, j2):
                hyp_token = colored(seq2[i].upper(), 'red')
                hyp_tokens.append(hyp_token)
        # More complicated logic for a substitution
        elif tag == 'replace':
            seq1_len = i2 - i1
            seq2_len = j2 - j1
            # Get a list of tokens for each
            s1 = list(map(str.upper, seq1[i1:i2]))
            s2 = list(map(str.upper, seq2[j1:j2]))
            # Pad the two lists with False values to get them to the same length
            if seq1_len > seq2_len:
                for i in range(0, seq1_len - seq2_len):
                    s2.append(False)
            if seq1_len < seq2_len:
                for i in range(0, seq2_len - seq1_len):
                    s1.append(False)
            assert(len(s1) == len(s2))
            # Pair up words with their substitutions, or fillers
            for i in range(0, len(s1)):
                w1 = s1[i]
                w2 = s2[i]
                # If we have two words, make them the same length
                if w1 and w2:
                    if len(w1) > len(w2):
                        s2[i] = w2 + ' ' * (len(w1) - len(w2))
                    elif len(w1) < len(w2):
                        s1[i] = w1 + ' ' * (len(w2) - len(w1))
                # Otherwise, create an empty filler word of the right width
                if not w1:
                    s1[i] = '*' * len(w2)
                if not w2:
                    s2[i] = '*' * len(w1)
            s1 = map(lambda x: colored(x, 'red'), s1)
            s2 = map(lambda x: colored(x, 'red'), s2)
            ref_tokens += s1
            hyp_tokens += s2
    if prefix1: ref_tokens.insert(0, prefix1)
    if prefix2: hyp_tokens.insert(0, prefix2)
    if suffix1: ref_tokens.append(suffix1)
    if suffix2: hyp_tokens.append(suffix2)    
    print(' '.join(ref_tokens))
    print(' '.join(hyp_tokens))

def mean(seq):
    """Return the average of the elements of a sequence."""
    return float(sum(seq)) / len(seq) if len(seq) > 0 else float('nan')

def print_wer_vs_length():
    """Print the average word error rate for each length sentence."""
    values = wer_bins.values()
    avg_wers = map(lambda x: (x[0], mean(x[1])), values)
    for length, avg in sorted(avg_wers, key=lambda x: x[1]):
        print('{0:5d} {1:f}'.format(i, avg_wers[i]))
    print('')

def plot_wers():
    """Plotting the results in this way is not helpful.
    however there are probably other useful plots we
    could use."""
    # Create a figure with size 6 x 6 inches.
    fig = Figure(figsize=(6, 6))
    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)
    # Create a subplot.
    ax = fig.add_subplot(111)
    # Set the title.
    ax.set_title('WER vs sentence length', fontsize=14)
    # Set the X Axis label.
    ax.set_xlabel('sentence length (# of words)', fontsize=12)
    # Set the Y Axis label.
    ax.set_ylabel('WER', fontsize=12)
    # Display Grid.
    # ax.grid(True,linestyle='-',color='0.75')
    # Generate the Scatter Plot.
    # ax.scatter(lengths, error_rates, s=20,color='tomato');
    ax.scatter(lengths, error_rates, color='tomato')
    # Save the generated Scatter Plot to a PNG file.
    canvas.print_figure('wer-vs-length.png', dpi=500)
