#
# MIT License
# 
# Copyright (c) 2018 SimBioSys, Inc.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

# External Includes
import collections
import csv
import json
import os
import re
import sys

# Internal Includes


try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class Reader(object):
    """...

    Args:
        - maffile (:py:obj:`str` or :py:obj:`File`): 
        - version (:py:obj:`str`): Version required to read; Currently unused.

    Attributes:
        - (): 
    """
    def __init__(self, maffile, version="2.4.1"):
        super(Reader, self).__init__()
        # Local attributes
        self.file = maffile
        self.isProtected = False

        # Do some processing
        if isinstance(maffile,str):
            self.file = open(maffile)
        if ".protected.maf" in self.file.name:
            self.isProtected = True

    def __iter__(self):
        return self

    def next(self):
        '''Return the next record in the file'''
        pass
