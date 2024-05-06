thisdir = 'stuff'

pyfiles = [
  '__init__.py',
  'test_thing.py',
]

py.install_sources(
  pyfiles,
  pure: false,
  subdir: thisdir,
)

py.extension_module(
  'thing',
  'thing.pyx',
  dependencies: py_dep,
  install: true,
  subdir: thisdir,
)
