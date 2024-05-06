from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

packages = [
    'stuff',
]

ext = Extension(
    'stuff.thing',
    ['src/stuff/thing.pyx'],
    define_macros = [('CYTHON_TRACE', 1)],
)

ext_modules = cythonize([ext], compiler_directives={'linetrace': True})

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    packages=packages,
    package_dir={'': 'src'},
)
