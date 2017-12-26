# Copyright 2013-2018 Ben Lambert

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
