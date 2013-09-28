from pytzpure.config import DEFAULT_TZ_MODULE_PREFIX, \
                            DEFAULT_ZONETAB_MODULE_NAME
from pytzpure.get_as_python import get_as_python
from pytzpure.loader import load_module
from pytzpure.lazy import LazyDict


class ZoneTabLazy(LazyDict):
    def __call__(self, iso3166_code):
        """Backwards compatibility."""
        return self[iso3166_code]

    def _fill(self):
        self.data = ZoneTabData.load_from_file().data


class ZoneTabData(object):
    def __init__(self, data):
        self.__data = data

    @classmethod
    def create_from_original(cls, pytz_container):

        # Induce the container to load.
        len(pytz_container)

        return cls(pytz_container.data)

    @classmethod
    def load_from_file(cls, module_name=DEFAULT_ZONETAB_MODULE_NAME, \
                       module_prefix=DEFAULT_TZ_MODULE_PREFIX):
        module = load_module(module_name, module_prefix)
        return cls(module.ztd)

    @property
    def as_python(self):
        return get_as_python({ 'ztd': self.__data })

    @property
    def data(self):
        return self.__data

