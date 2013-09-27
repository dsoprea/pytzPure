from pytzpure.config import DEFAULT_TZ_MODULE_PREFIX, \
                            DEFAULT_ISO3166_MODULE_NAME
from pytzpure.get_as_python import get_as_python
from pytzpure.loader import load_module


class Iso3166Lazy(LazyDict):
    def _fill(self):
        self.data = Iso3166Data.load_from_file.data


class Iso3166Data(object):
    @classmethod
    def create_from_original(cls, pytz_container):
        self.__data = pytz_container.data

    @classmethod
    def load_from_file(cls, module_name=DEFAULT_ZONETAB_MODULE_NAME, \
                       module_prefix=DEFAULT_TZ_MODULE_PREFIX):
        module = load_module(module_name, module_prefix)
        return module.i3d

    @property
    def as_python(self):
        return get_as_python({ 'i3d': self.__data })

    @property
    def data(self):
        return self.__data

