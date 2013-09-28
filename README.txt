Introduction
------------

"pytzpure" is a pure-Python adaptation of "pytz", the standard timezone library
for Python. 

My particular use-case was that I needed timezone support in an AppEngine 
environment, where there's no support for data files.


Requirements
------------

pytz: Only required prior to build.


Install
-------

Build the required data files (requires "pytz"). This converts the system's 
zoneinfo data to Python modules.

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

Use timezones with "datetime":

    ../pytzpure$ PYTHONPATH=.:/tmp python
    Python 2.7.4 (default, Apr 19 2013, 18:32:33) 
    [GCC 4.7.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from datetime import datetime
    >>> from pytzpure import timezone
    >>> utc = timezone('UTC')
    >>> detroit = timezone('America/Detroit')
    >>> datetime.utcnow().replace(tzinfo=utc).astimezone(detroit).\
            strftime('%H:%M:%S %z')
    '16:34:37 -0400'

List potential timezones:

    >>> from pytzpure import all_timezones
    >>> print(all_timezones[:10])
    ['Africa/Abidjan', 'Africa/Accra', 'Africa/Addis_Ababa', 'Africa/Algiers', 
     'Africa/Asmara', 'Africa/Asmera', 'Africa/Bamako', 'Africa/Bangui', 
     'Africa/Banjul', 'Africa/Bissau']

NOTE: that the list of timezones only lists what is available, and, therefore, 
what can be used with timezone(). You are welcome to physically remove any of 
the built timezone files that you don't have a need for.

List countries and their ISO acronyms:

    >>> from pytzpure import country_names
    >>> print(dict([(k, country_names[k]) for k in country_names.keys()[:10]]))
    {'GW': 'Guinea-Bissau', 'WF': 'Wallis & Futuna', 'GU': 'Guam', 
     'GT': 'Guatemala', 'GS': 'South Georgia & the South Sandwich Islands', 
     'JP': 'Japan', 'JM': 'Jamaica', 'JO': 'Jordan', 'WS': 'Samoa (western)', 
     'JE': 'Jersey'}

List countries' ISO acronyms and their timezones:

    >>> from pytzpure import country_timezones
    >>> print(dict([(k, country_timezones[k]) \
                    for k \
                    in country_timezones.keys()[:10]]))
    {'GW': ['Africa/Bissau'], 'WF': ['Pacific/Wallis'], 'GU': ['Pacific/Guam'], 
     'GT': ['America/Guatemala'], 'GS': ['Atlantic/South_Georgia'], 
     'JP': ['Asia/Tokyo'], 'JM': ['America/Jamaica'], 'JO': ['Asia/Amman'], 
     'WS': ['Pacific/Apia'], 'JE': ['Europe/Jersey']}

