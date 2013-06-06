============
asr_evalution
============

Python module for evaluting ASR hypotheses (i.e. word error rate and word recognition rate).

This module depends on my editdistance project, for computing edit distances between arbitrary sequences.

The formatting of the output of this program is very loosely based around the same idea as the align.c program commonly used within the Sphinx ASR community.

This may run a bit faster if neither instances nor confusions are printed.

Command line usage
------------------

For command line usage, see:

    python editdistance.py --help

It should be something like this:

    
    usage: asr_evaluation.py [-h] [-i] [-id] [-c] [-p] [-m count] ref hyp
    
    Evaluate an ASR transcript against a reference transcript.
    
    positional arguments:
      ref                   the reference transcript filename
      hyp                   the ASR hypothesis filename
    
    optional arguments:
      -h, --help            show this help message and exit
      -i, --print-instances
                            print the individual sentences and their errors
      -id, --has-ids        hypothesis and reference files have ids in the last
                            token?
      -c, --confusions      print tables of which words were confused
      -p, --print-wer-vs-length
                            print table of average WER grouped by reference
                            sentence length
      -m count, --min-word-count count
                            minimum word count to show a word in confusions



This requires Python 2.7+ since it uses argparse for the command line interface.  The rest of the code should be OK with earlier versions of Python
