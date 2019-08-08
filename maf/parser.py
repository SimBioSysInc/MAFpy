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
from collections import OrderedDict
import csv
import json
import os
import re
import sys

_columnHeaders = {}

class Reader(object):
    """...

    Args:
        - maffile (:py:obj:`str` or :py:obj:`File`): Path to a file, or a file pointer.
        - version (:py:obj:`str`): Version required to read; currently unused.
        - validate (:py:obj:`bool`): Whether or not to validate the file (False speeds up file loading).

    Attributes:
        - file (:py:obj:`File`): Inner representation of a file
        - isProtected (:py:obj:`bool`): Whether or not the MAF file contains personally identifiable data (e.g., ends with "*.protected.maf").
        - version (:py:obj:`str`): Version of the file to open, defaults to 2.4.1. The reader will attempt to use the correct version, however, this is the version that will be used for validation.
        - metadata (:py:obj:`dict`): 
        - optionalHeader (:py:obj:`list`):
    """
    def __init__(self, maffile, version="2.4.1", validate=False):
        # Load column headers
        global _columnHeaders
        if version not in _columnHeaders:
            colFile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   "column_headers_%s.json"%(version.replace(".","_")))
            _columnHeaders[version] = json.load(open(colFile, "r"))

        super(Reader, self).__init__()
        # Local attributes
        self.file = maffile
        self.isProtected = False
        self.version = version
        self.metadata = {}
        self.optionalHeaders = []

        # Do some processing
        if isinstance(maffile,str):
            self.file = open(maffile)
        if ".protected.maf" in self.file.name:
            self.isProtected = True

        # Do validation
        if validate:
            validated, errs = self._validate()
            if not validated:
                self.file.seek(0)
                raise Warning("MAF file did not pass validation. You can still use it, but beware. Errors:\n%s"%("\n\t".join(errs)))
        self.file.seek(0)

        # Read header
        self._parseHeader()

    def __iter__(self):
        return self

    def __next__(self):
        '''Return the next record in the file'''
        nextLine = next(self.file)
        if nextLine != None:
            return self._parseLine(nextLine)

    def _parseHeader(self):
        # Parses the header comments in the file and stores them in the "metadata" attribute
        for line in self.file:
            if line[0] != "#":
                # Extract header fields (it should be the first line after all the comments/metadata)
                self.optionalHeaders = line.rstrip("\n").split("\t")[34:]

                # Done reading header
                break
            else:
                # Extract metadata (lines beginning with "#"
                name, data = line[1:-1].split(" ")
                self.metadata[name] = data

    def _parseLine(self, line):
        # _parseLine: Parses an individual line and returns the results in an easy to use dict format
        global _columnHeaders
        ls = line.rstrip("\n").split("\t")
        toReturn = {}
        for index, infoHeader in _columnHeaders[self.version].items():
            if infoHeader["header"] in ["Start_Position", "End_Position"]:
                toReturn[infoHeader["header"]] = int(ls[int(index)-1])
            else:
                toReturn[infoHeader["header"]] = ls[int(index)-1]
        return toReturn

    def _validate(self):
        global _columnHeaders

        # List of errors
        validationErrors = []

        # Go to beginning of file
        self.file.seek(0)

        # Version line
        firstLine = next(self.file)
        if firstLine != "#version %s\n"%(self.version):
            validationErrors.append("Version header incorrect; expected version %s"%(self.version))

        # Skip rest of comment lines
        header = next(self.file)
        while header[0] == "#":
            header = next(self.file)
        # Check for order of required fields
        countCorrect = 0
        headerFields = header.rstrip("\n").split("\t")
        for index, headerInfo in _columnHeaders[self.version].items():
            if headerFields[int(index)-1] != headerInfo["header"]:
                validationErrors.append("Incorrect header at %s, expected: '%s' got: '%s'"%(index, headerInfo["header"], headerFields[int(index)-1]))
            else:
                countCorrect += 1
        if countCorrect != len(headerFields):
            validationErrors.append("Not all required header fields were included. %d missing"%(len(headerFields)-countCorrect))

        mutationStatusIdx = None
        validationStatusIdx = None
        verificationStatusIdx = None
        variantClassificationIdx = None
        for index, headerInfo in _columnHeaders[self.version].items():
            if headerInfo["header"] == "Mutation_Status":
                mutationStatusIdx = int(index)-1
            if headerInfo["header"] == "Validation_Status":
                validationStatusIdx = int(index)-1
            if headerInfo["header"] == "Verification_Status":
                verificationStatusIdx = int(index)-1
            if headerInfo["header"] == "Variant_Classification":
                variantClassificationIdx = int(index)-1

        # Check each lines for correct form
        lineNumber = 0
        for line in self.file:
            ls = line.rstrip("\n").split("\t")

            # Check that the somatic field  field
            if not self.isProtected:
                A = ls[mutationStatusIdx] == "Somatic"
                B = ls[validationStatusIdx] == "Valid"
                C = ls[verificationStatusIdx] == "Verified"
                D = ls[variantClassificationIdx] in ["Frame_Shift_Del",
                                                     "Frame_Shift_Ins",
                                                     "In_Frame_Del",
                                                     "In_Frame_Ins",
                                                     "Missense_Mutation",
                                                     "Nonsense_Mutation",
                                                     "Silent",
                                                     "Splice_Site",
                                                     "Translation_Start_Site",
                                                     "Nonstop_Mutation",
                                                     "RNA",
                                                     "Targeted_Region"]
                E = ls[mutationStatusIdx] == "None"
                F = ls[validationStatusIdx] == "Invalid"
                somaticRule = (A and (B or C or D)) or (E and F)
                if not somaticRule:
                    validationErrors.append("Incorrect somatic specification on line: %d. See the MAF specification for details."%(lineNumber))

            # Validate Strand
            if ls[7] != "+":
                validationErrors.append("Incorrect Strand on line: %d"%(lineNumber))

            # Check for valid sets
            for index, headerInfo in _columnHeaders[self.version].items():
                if "Set" in headerInfo["enumerated"]:
                    continue
                elif "No" in headerInfo["enumerated"]:
                    continue
                elif "" == headerInfo["enumerated"]:
                    continue
                elif headerInfo["null"]:
                    if ls[int(index)-1] == "":
                        continue
                elif headerInfo["enumerated"] == ["A","C","T","G","-"]:
                    if not all([x in ["A","C","T","G","-"] for x in ls[int(index)-1]]):
                        validationErrors.append("Incorrect sequence value in field %s on line %d"%(headerInfo[""], lineNumber))
                else:
                    if ls[int(index)-1] not in headerInfo["enumerated"]:
                        validationErrors.append("Incorrect value in field %s on line %d"%(headerInfo["header"], lineNumber))

            # TODO: Additional MAF file checks

            # Update current line number
            lineNumber += 1

        # Check header
        if len(validationErrors) > 0:
            return False, validationErrors
        return True, None



# Another name for the reader
MAFReader = Reader



if __name__ == "__main__":
    # Parse and validate file
    filename = sys.argv[1]
    Reader(filename, validate=True)


