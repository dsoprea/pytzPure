from imp import find_module
from os import environ

from pytzpure.config import DEFAULT_TZ_MODULE_PREFIX

def _get_fq_module_name(module_name, module_prefix=DEFAULT_TZ_MODULE_PREFIX):

    # This only applies when we receive a zone-name.
    module_name = module_name.replace('/', '.')

    fq_module_name = ('%s.%s' % (module_prefix, module_name)) \
                     if module_prefix is not None \
                     else zone_module_name

    return fq_module_name

def is_loadable(module_name, module_prefix=DEFAULT_TZ_MODULE_PREFIX):
    fq_module = _get_fq_module_name(module_name, module_prefix)

    try:
        __import__(fq_module)
    except ImportError:
        return False
    else:
        return True

def load_module(module_name, module_prefix=DEFAULT_TZ_MODULE_PREFIX):
    fq_module_name = _get_fq_module_name(module_name, module_prefix)

    period_at = fq_module_name.rfind('.')
    if period_at == -1:
        module_name = fq_module_name
    else:
        module_name = fq_module_name[period_at + 1:]
    
    module = __import__(fq_module_name, fromlist=[module_name])
    return module

