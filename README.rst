
blanket
=======

Blanket is an extension to reStructuredText and Sphinx to be able to read and
render coverage data.  Blanket is able to render the output from gcovr (version 4.2)
and llvm show (version 8) to create docutils documentation.

Usage
-----

::

  .. coverage:: coverage.dat

where *coverage.dat* is a data file containing gcovr output or llvm show output.  The data
file is considered relative to the *conf.py* file if the path is not absolute.

The *coverage* directive also has a *summary* option that provides a short statement on
the coverage statistics::

  .. coverage:: coverage.dat
     :summary:

