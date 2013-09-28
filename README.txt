Install
-------

Build the data files (uses "pytz"):

    $ PYTHONPATH=. python pytzpure/tools/tz_export.py /tmp/pytzpp
    Verifying export path exists: /tmp/pytzpp
    Verifying __init__.py .
    Writing zone tree.
    (578) timezones written.
    Writing country timezones.
    Writing country names.

Though I wrote everything with a sense of flexibility in how things are found, 
it's still going to be a headache to rewire. It's recommended that the files 
are always built under a directory named "pytzpp".


Usage
-----

The usage pattern is identical to "pytz". However, make sure that the root 
directory of the "pytzpp" directory (/tmp, above) is in the PYTHONPATH.


