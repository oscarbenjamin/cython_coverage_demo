project('stuff', 'cython', 'c')

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

cc = meson.get_compiler('c')

if get_option('coverage')
  add_project_arguments('-X', 'linetrace=True', language : 'cython')
  add_project_arguments('-DCYTHON_TRACE=1', language : 'c')
endif

subdir('src/stuff')
