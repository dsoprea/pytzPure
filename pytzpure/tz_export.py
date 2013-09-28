"""This module calls the version of "pytz" that is in the path, the original
"pytz", to get the original data. Our versions only know how to read it, once
exported, as Python modules.
"""

import json

from os import path, utime, mkdir
from inspect import getmro

from pytz import timezone, all_timezones, country_timezones, country_names

from pytzpure.config import DEFAULT_ZONETAB_MODULE_NAME, \
                            DEFAULT_ISO3166_MODULE_NAME
from pytzpure.tz_descriptor import TzDescriptor
from pytzpure.zone_tab_data import ZoneTabData
from pytzpure.iso3166_data import Iso3166Data


class TzTranslate(object):
    """An iterable that moves through the supports timezone objects, and wraps 
    them in our conversion class.
    """

    def __init__(self):
        self.__all_timezones = iter(all_timezones)

    def __iter__(self):
        return self

    def __next__(self):
        next_tz_name = self.__all_timezones.next()

        tz_info = timezone(next_tz_name)
        return TzDescriptor.create_from_pytz(tz_info)

    next = __next__

def _touch(file_path):
    with file(file_path, 'w') as f:
        pass

def _get_path_info_from_name(zone_name):
    parts = zone_name.split('/')
    dir_parts = parts[:-1]

    if dir_parts:
        zone_path = path.join(*dir_parts)
    else:
        zone_path = '.'

    filename = ('%s.py' % (parts[-1]))

    return (zone_path, filename)

def write_zone_tree(root_path):
    seen_paths = set()
    i = 0
    for tz_info in TzTranslate():
        (zone_path, filename) = _get_path_info_from_name(tz_info.zone_name)
        full_path = path.join(root_path, zone_path)
        file_path = path.join(full_path, filename)
        
        code = tz_info.as_python

        if full_path not in seen_paths:
            try:
                mkdir(full_path)
            except OSError:
                pass
            finally:
                _touch(path.join(full_path, '__init__.py'))
                seen_paths.add(full_path)
        
        with open(file_path, 'w') as f:
            f.write(code)

        i += 1

    print("(%d) timezones written." % (i))

def _write_single_value_as_python(root_path, module_name, container):
    data_encoded = container.as_python

    file_path = path.join(root_path, ('%s.py' % (module_name)))
    with open(file_path, 'w') as f:
        f.write(data_encoded)

def write_country_timezones(root_path, module_name=DEFAULT_ZONETAB_MODULE_NAME):
    ztd = ZoneTabData.create_from_original(country_timezones)
    _write_single_value_as_python(root_path, module_name, ztd)

def write_country_names(root_path, module_name=DEFAULT_ISO3166_MODULE_NAME):
    i3d = Iso3166Data.create_from_original(country_names)
    _write_single_value_as_python(root_path, module_name, i3d)

def export(root_path):
    print("Verifying export path exists: %s" % (root_path))

    try:
        mkdir(root_path)
    except OSError:
        pass

    print("Verifying __init__.py .")
    _touch(path.join(root_path, '__init__.py'))

    print("Writing zone tree.")
    write_zone_tree(root_path)

    print("Writing country timezones.")
    write_country_timezones(root_path)

    print("Writing country names.")
    write_country_names(root_path)

