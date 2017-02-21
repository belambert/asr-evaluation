==============
asr_evaluation
==============

[![Build Status](https://travis-ci.org/belambert/asr-evaluation.svg?branch=master)](https://travis-ci.org/belambert/asr-evaluation)
[![PyPI version](https://badge.fury.io/py/asr_evaluation.svg)](https://badge.fury.io/py/asr_evaluation)
[![Coverage Status](https://coveralls.io/repos/github/belambert/asr-evaluation/badge.svg?branch=master)](https://coveralls.io/github/belambert/asr-evaluation?branch=master)

Python module for evaluting ASR hypotheses (i.e. word error rate and word 
recognition rate).

This module depends on my editdistance project, for computing edit distances 
between arbitrary sequences.

The formatting of the output of this program is very loosely based around the 
same idea as the align.c program commonly used within the Sphinx ASR community. 
 This may run a bit faster if neither instances nor confusions are printed.

Please let me know if you have any comments, questions, or problems.

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
    python bin/evaluate.py --help
```

It should be something like this:

```    
    usage: evaluate.py [-h] [-i] [-id] [-c] [-p] [-m count] ref hyp
    
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
```

