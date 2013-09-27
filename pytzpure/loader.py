from imp import find_module

from pytzpure.config import DEFAULT_TZ_MODULE_PREFIX

def _get_fq_module_name(zone_name, module_prefix=DEFAULT_TZ_MODULE_PREFIX):
    zone_module_name = zone_name.replace('/', '.')
    fq_module_name = ('%s.%s' % (module_prefix, zone_module_name)) \
                     if module_prefix is not None \
                     else zone_module_name

    return fq_module_name

def is_loadable(zone_name, module_prefix=DEFAULT_TZ_MODULE_PREFIX):
    try:
        find_module(_get_fq_module_name(zone_name, module_prefix))
    except ImportError:
        return False
    else:
        return True

def load_module(zone_name, module_prefix=DEFAULT_TZ_MODULE_PREFIX):
    fq_module_name = _get_fq_module_name(zone_name, module_prefix)

    period_at = fq_module_name.rfind('.')
    if period_at == -1:
        module_name = fq_module_name
    else:
        module_name = fq_module_name[period_at + 1:]
    
    module = __import__(fq_module_name, fromlist=[module_name])
    return module

