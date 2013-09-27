import json

from os import path, environ
from inspect import getmro
from datetime import datetime, timedelta
from time import mktime
from imp import find_module

from pytzpure.utility.get_as_python import get_as_python

_DEFAULT_TZ_MODULE_PREFIX = environ.get('TZ_MODULE_PREFIX', 'tzppdata')


class TzDescriptor(object):
    def __init__(self, zone_name, parent_class_name, 
                 utc_transition_times_list=None, transition_info_list=None, 
                 utcoffset=None, tzname=None):

        self.__zone_name = zone_name
        self.__parent_class_name = parent_class_name
        self.__utc_transition_times_list = utc_transition_times_list
        self.__transition_info_list = transition_info_list
        self.__utcoffset = utcoffset
        self.__tzname = tzname

    def __str__(self):
        return ('<%s>' % (self.__zone_name))

    @classmethod
    def get_path_info_from_name(cls, zone_name):
        parts = zone_name.split('/')
        dir_parts = parts[:-1]

        if dir_parts:
            zone_path = path.join(*dir_parts)
        else:
            zone_path = '.'

        filename = ('%s.py' % (parts[-1]))

        return (zone_path, filename)

    @classmethod
    def get_fq_module_name(cls, zone_name, 
                           module_prefix=_DEFAULT_TZ_MODULE_PREFIX):
        (path, filename) = cls.get_path_info_from_name(zone_name)

        zone_module_name = zone_name.replace('/', '.')
        fq_module_name = ('%s.%s' % (module_prefix, zone_module_name)) \
                         if module_prefix is not None \
                         else zone_module_name

        return fq_module_name

    @classmethod
    def is_loadable(cls, zone_name, module_prefix=_DEFAULT_TZ_MODULE_PREFIX):
        try:
            find_module(cls.get_fq_module_name(zone_name, module_prefix))
        except ImportError:
            return False
        else:
            return True

    @classmethod
    def load_from_file(cls, zone_name, 
                       module_prefix=_DEFAULT_TZ_MODULE_PREFIX):
        fq_module_name = cls.get_fq_module_name(zone_name, module_prefix)

        period_at = fq_module_name.rfind('.')
        if period_at == -1:
            module_name = fq_module_name
        else:
            module_name = fq_module_name[period_at + 1:]
        
        module = __import__(fq_module_name, fromlist=[module_name])

        return cls(module.zone_name, 
                   module.parent_class_name,
                   module.utc_transition_times_list, 
                   module.transition_info_list,
                   module.utcoffset, 
                   module.tzname)

    @classmethod
    def create_from_pytz(cls, tz_info):
        """Create an instance using the result of the timezone() call in 
        "pytz".
        """

        zone_name = tz_info.zone

        utc_transition_times_list_raw = getattr(tz_info, 
                                                '_utc_transition_times', 
                                                None)

        utc_transition_times_list = [tuple(utt.timetuple()) 
                                     for utt 
                                     in utc_transition_times_list_raw] \
                                    if utc_transition_times_list_raw is not None \
                                    else None
        
        transition_info_list_raw = getattr(tz_info, 
                                           '_transition_info', 
                                           None)

        transition_info_list = [(utcoffset_td.total_seconds(), 
                                 dst_td.total_seconds(), 
                                 tzname)
                                for (utcoffset_td, dst_td, tzname)
                                in transition_info_list_raw] \
                               if transition_info_list_raw is not None \
                               else None

        utcoffset = getattr(tz_info, '_utcoffset', None)
        tzname = getattr(tz_info, '_tzname', None)

        parent_class_name = getmro(tz_info.__class__)[1].__name__
        return cls(zone_name, parent_class_name, utc_transition_times_list, 
                   transition_info_list, utcoffset, tzname)

    @property
    def zone_name(self):
        return self.__zone_name

    @property
    def parent_class_name(self):
        return self.__parent_class_name
    
    @property
    def utc_transition_times_list(self):
        return self.__utc_transition_times_list
    
    @property
    def utc_transition_times_list_formal(self):
        try:
            return self.__uttl
        except AttributeError:
            translate = lambda dt_tuple: datetime.utcfromtimestamp(mktime(dt_tuple))

            self.__uttl = [translate(dt_tuple) \
                           for dt_tuple \
                           in self.__utc_transition_times_list]
    
            return self.__uttl
    
    @property
    def transition_info_list_formal(self):
        try:
            return self.__til
        except AttributeError:
            self.__til = [(timedelta(seconds=utcoffset_seconds), 
                           timedelta(seconds=dst_seconds), 
                           tzname) 
                          for (utcoffset_seconds, dst_seconds, tzname) 
                          in self.__transition_info_list]

            return self.__til

    @property
    def utcoffset(self):
        return self.__utcoffset
    
    @property
    def tzname(self):
        return self.__tzname

    @property
    def as_json(self):
        try:
            return self.__json
        except AttributeError:
            self.__json = json.dumps((self.__zone_name, 
                                      self.__utc_transition_times_list, 
                                      self.__transition_info_list,
                                      self.__utcoffset,
                                      self.__tzname))

            return self.__json

    @property
    def as_python(self):
        try:
            return self.__python
        except AttributeError:
            data = { 'zone_name': self.__zone_name,
                     'parent_class_name': self.__parent_class_name,
                     'utc_transition_times_list': self.__utc_transition_times_list,
                     'transition_info_list': self.__transition_info_list,
                     'utcoffset': self.__utcoffset,
                     'tzname': self.__tzname }

            self.__python = get_as_python(data)
            return self.__python

