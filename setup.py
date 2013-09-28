from setuptools import setup, find_packages
import sys, os

version = '0.2.1'

setup(name='pytzpure',
      version=version,
      description="A pure-Python version of PYTZ (timezones).",
      long_description="""\A variation of PYTZ (standard timezone support) that allows an export of the standard zoneinfo data to Python modules, and then reads all further data from those via all of the standard PYTZ calls. This allows usage from pure-Python-only environments, such as Google AppEngine.
""",
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Software Development :: Libraries :: Python Modules'], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='timezone timezones olson pytz purepython pure-python',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/PyTzPure',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'pytz'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

