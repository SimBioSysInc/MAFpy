Introduction to MAFpy
=====================

The Mutation Annotation Format (MAF) is a tab-delimited file format describing somatic and/or germilne mutation annotations. These files are commonly found in online databases such as The Cancer Genome Atlas (`TCGA <https://cancergenome.nih.gov/>`_). The files contain a number of required columns describing the nature of the mutations along with optional columns. A full description of the format can be found at on the National Cancer Institute's (NCI) `website <https://wiki.nci.nih.gov/display/TCGA/Mutation+Annotation+Format+%28MAF%29+Specification>`_. 

MAFpy reads and/or validates MAF files. It is designed to work similarly to the `cvs <https://docs.python.org/3.6/library/csv.html>`_ reader from the standard library. The code is licensed under the `MIT license <https://opensource.org/licenses/MIT>`_.


Installation
============

MAFpy is designed for Python 3.0 and above. While it may work with Python 2.5+ with
minimal modifications, these versions will not be supported.

Distributions of the library can be found on the PyPI repository and easily installed via::

    pip install mafpy

Support
=======
MAFpy is developed by `SimBioSys, Inc. <http://www.simbiosys.tech>`_. To get support or report an issue please visit the `GitHub issues page <https://github.com/SimBioSysInc/MAFpy/issues>`_


