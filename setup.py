from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='pytzpure',
      version=version,
      description="Produce pure-Python Olson timezone data/files.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='olson timezones time-zones purepython pure-python',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://www.github.com/dsoprea/PyTzPure',
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
