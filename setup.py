from setuptools import setup
from setuptools.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext = Extension(
    'stuff',
    ['src/stuff.pyx'],
    define_macros = [('CYTHON_TRACE', 1)],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize([ext], compiler_directives={'linetrace': True}),
    package_dir={'': 'src'},
)
