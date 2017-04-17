"""
Unit tests for asr_evaluation.
"""
from __future__ import division

import sys
import unittest

from asr_evaluation import __main__

# Note these tests aren't checking for correctness.  They are simply
# exercising all the command line options to make sure we don't get errors
# simply by running them.

class TestASREvaluation(unittest.TestCase):
    """..."""

    def testing(self):
        """..."""
        self.assertTrue(True)

    def test_cli1(self):
        sys.argv = ['evaluate.py', 'requirements.txt', 'setup.py', '-c', '-m', '0', '-i']
        __main__.main()

    def test_cli2(self):
        sys.argv = ['evaluate.py', 'requirements.txtssssss', 'setup.py', '-c', '-m', '0', '-i']
        with self.assertRaises(SystemExit):
            __main__.main()

    def test_cli3(self):
        sys.argv = ['evaluate.py', 'requirements.txt', 'setup.py', '-c', '-m', '0']
        __main__.main()

    def test_cli4(self):
        sys.argv = ['evaluate.py', 'requirements.txt', 'setup.py']
        __main__.main()

    def test_cli5(self):
        sys.argv = ['evaluate.py', 'setup.py', 'setup.py']
        __main__.main()

    def test_cli6(self):
        sys.argv = ['evaluate.py', 'setup.py', 'setup.py', '-a']
        __main__.main()

    def test_cli7(self):
        sys.argv = ['evaluate.py', 'setup.py', 'setup.py', '-e']
        __main__.main()

    def test_cli8(self):
        sys.argv = ['evaluate.py', 'requirements.txt', 'requirements.txt', '-id']
        __main__.main()
