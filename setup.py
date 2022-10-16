import sys
import os
import numpy

from distutils.core import Extension, setup

modules = ["numba_test"]
sources = {name: [name + "_wrap.cxx"] for name in modules}
macros = [('TARGET_PY3', '1'), ('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]

proxy_names = {name: '_'+name for name in modules}
ext_modules = [Extension(proxy_names[name],
                                  sources=sources[name],
                                  extra_link_args = [],
                                  define_macros=macros)
                   for name in modules]


setup (name = 'numba_test',
       author      = "S.Shiraiwa",
       description = """numba test""",
       ext_modules = ext_modules,
       py_modules = modules, )

