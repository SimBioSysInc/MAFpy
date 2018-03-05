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

from setuptools import setup
from distutils.extension import Extension
import sys


DEPENDENCIES = ["setuptools"]

# Get version from file
VERSION="Undefined"
for line in open('maf/__init__.py'):
    if line.startswith("VERSION"):
        exec(line.strip())

setup(
    name='MAFpy',
    packages=["maf", "maf.test"],
    scripts=[],
    author='Joseph R. Peterson',
    author_email='jrp@simbiosys.tech',
    description='Mutation Annotation Format (MAF) parser for Python',
    long_description='',
#    test_suite='',
    install_requires=DEPENDENCIES,
#    entry_points = {},
    url='https://github.com/SimBioSysInc/MAFpy',
    version=VERSION,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    keywords='bioinforamtics',
    include_package_data=True,
    package_data = {
        '': [
             '*.json',
             '*.maf',
            ],
    }
)

