asr_evaluation
==============
[![Build Status](https://travis-ci.org/belambert/asr-evaluation.svg?branch=master)](https://travis-ci.org/belambert/asr-evaluation)
[![PyPI version](https://badge.fury.io/py/asr_evaluation.svg)](https://badge.fury.io/py/asr_evaluation)
[![codecov](https://codecov.io/gh/belambert/asr-evaluation/branch/master/graph/badge.svg)](https://codecov.io/gh/belambert/asr-evaluation)

Python module for evaluting ASR hypotheses (i.e. word error rate and word 
recognition rate).

This module depends on the [editdistance](https://github.com/belambert/edit-distance)
project, for computing edit distances between arbitrary sequences.

The formatting of the output of this program is very loosely based around the 
same idea as the align.c program commonly used within the Sphinx ASR community. 
This may run a bit faster if neither instances nor confusions are printed.

Please let me know if you have any comments, questions, or problems.

Output
------
The program outputs three standard measurements:
 - [Word error rate (WER)](https://en.wikipedia.org/wiki/Word_error_rate)
 - Word recognition rate (the number of _matched_ words in the alignment divided by the number of words in the reference).
 - Sentence error rate (SER) (the number of incorrect sentences divided by the total number of sentences).


Installing & uninstalling
-------------------------
The easiest way to install is using pip:

    pip install asr-evaluation

Alternatively you can clone this git repo and install using distutils:

    git clone git@github.com:belambert/asr-evaluation.git
    cd asr-evaluation
    python setup.py install

To uninstall with pip:

    pip uninstall asr-evaluation


Command line usage
------------------
For command line usage, see:
```
    wer --help
```

It should display something like this:

```    
usage: wer [-h] [-i | -r] [--head-ids] [-id] [-c] [-p] [-m count] [-a] [-e]
           ref hyp

Evaluate an ASR transcript against a reference transcript.

positional arguments:
  ref                   Reference transcript filename
  hyp                   ASR hypothesis filename

optional arguments:
  -h, --help            show this help message and exit
  -i, --print-instances
                        Print all individual sentences and their errors.
  -r, --print-errors    Print all individual sentences that contain errors.
  --head-ids            Hypothesis and reference files have ids in the first
                        token? (Kaldi format)
  -id, --tail-ids, --has-ids
                        Hypothesis and reference files have ids in the last
                        token? (Sphinx format)
  -c, --confusions      Print tables of which words were confused.
  -p, --print-wer-vs-length
                        Print table of average WER grouped by reference
                        sentence length.
  -m count, --min-word-count count
                        Minimum word count to show a word in confusions.
  -a, --case-insensitive
                        Down-case the text before running the evaluation.
  -e, --remove-empty-refs
                        Skip over any examples where the reference is empty.
```

Contributing and code of conduct
--------------------------------
For contributions, it's best to Github issues and pull requests. Proper
testing and documentation suggested.

Code of conduct is expected to be reasonable, especially as specified by
the [Contributor Covenant](http://contributor-covenant.org/version/1/4/)
