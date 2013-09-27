import json

from os import path, utime, mkdir
from inspect import getmro
from pytz import timezone, all_timezones

from pytzpure.tz_descriptor import TzDescriptor


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
        return TzDescriptor.create_from_pytz(create_from_pytz)

    next = __next__

def _touch(file_path):
    with file(file_path, 'w') as f:
        pass

def build_tree(root_path):
    seen_paths = set()
    for tz_info in TzTranslate():
        (zone_path, filename) = TzDescriptor.\
                                    get_path_info_from_name(tz_info.zone_name)
        full_path = path.join(root_path, zone_path)
        file_path = path.join(full_path, filename)
        
        code = tz_info.as_python

        if full_path not in seen_paths:
            try:
                mkdir(full_path)
            except OSError:
                pass
            finally:
                touch_file_path = path.join(full_path, '__init__.py')
                _touch(touch_file_path)
                seen_paths.add(full_path)
        
        with file(file_path, 'w') as f:
            f.write(code)

try:
    mkdir('/tmp/tz')
except OSError:
    pass

build_tree('/tmp/tz')
#
#print(TzDescriptor.load_from_file('America/Detroit', module_prefix='tz'))

