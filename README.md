# Coverage measurement of Cython code with spin/meson vs setuptools

## setuptools

To measure coverage measurement with setuptools we can make an inplace build
and then run pytest with `--cov`:

```console
$ python setup.py build_ext --inplace
...
$ PYTHONPATH=src pytest --cov=stuff --pyargs stuff
======================================== test session starts ========================================
platform linux -- Python 3.11.3, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/oscar/current/active/cython_coverage_demo
configfile: pyproject.toml
plugins: cov-5.0.0
collected 1 item                                                                                    

src/stuff/test_thing.py .                                                                     [100%]

---------- coverage: platform linux, python 3.11.3-final-0 -----------
Name                      Stmts   Miss  Cover
---------------------------------------------
src/stuff/__init__.py         0      0   100%
src/stuff/test_thing.py       4      0   100%
src/stuff/thing.pyx           2      0   100%
---------------------------------------------
TOTAL                         6      0   100%


========================================= 1 passed in 0.08s =========================================
```

Note that we get coverage measurement for `thing.pyx`.

## spin/meson

**Make sure to run `./clean.sh` after using `./coverage_setuptools.sh`.**

There are different ways to measure coverage with `spin/meson`. First we can
use `spin test`:

```console
$ spin build --clean -- -Dcoverage=true
...
$ spin test --coverage
======================================== test session starts ========================================
platform linux -- Python 3.11.3, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/oscar/current/active/cython_coverage_demo/build-install/usr/lib/python3.11/site-packages
configfile: ../../../../../pyproject.toml
plugins: cov-5.0.0
collected 1 item                                                                                    

stuff/test_thing.py .                                                                         [100%]

---------- coverage: platform linux, python 3.11.3-final-0 -----------
Name                  Stmts   Miss  Cover
-----------------------------------------
stuff/__init__.py         0      0   100%
stuff/test_thing.py       4      0   100%
-----------------------------------------
TOTAL                     4      0   100%
Coverage HTML written to dir /home/oscar/current/active/cython_coverage_demo/build/coverage/


========================================= 1 passed in 0.10s =========================================
```

Note that `thing.pyx` is not mentioned in the coverage report.

We can ask `spin` to run pytest with our command line:

```console
$ spin run pytest --cov=stuff --pyargs stuff
 $ meson compile -C build
 $ meson install --only-changed -C build --destdir ../build-install
======================================== test session starts ========================================
platform linux -- Python 3.11.3, pytest-8.2.0, pluggy-1.5.0
rootdir: /home/oscar/current/active/cython_coverage_demo
configfile: pyproject.toml
plugins: cov-5.0.0
collected 1 item                                                                                    

build-install/usr/lib/python3.11/site-packages/stuff/test_thing.py .                          [100%]

/home/oscar/.pyenv/versions/3.11.3/envs/cython_coverage_demo-3.11.git/lib/python3.11/site-packages/coverage/report_core.py:109:
    CoverageWarning: Couldn't parse Python file
    '/home/oscar/current/active/cython_coverage_demo/src/stuff/thing.pyx'
    (couldnt-parse) coverage._warn(msg, slug="couldnt-parse")
/home/oscar/.pyenv/versions/3.11.3/envs/cython_coverage_demo-3.11.git/lib/python3.11/site-packages/coverage/report_core.py:115:
    CoverageWarning: Couldn't parse
    '/home/oscar/current/active/cython_coverage_demo/thing.pyx': No source for
    code: '/home/oscar/current/active/cython_coverage_demo/thing.pyx'.
    (couldnt-parse) coverage._warn(msg, slug="couldnt-parse")

---------- coverage: platform linux, python 3.11.3-final-0 -----------
Name                                                                 Stmts   Miss  Cover
----------------------------------------------------------------------------------------
build-install/usr/lib/python3.11/site-packages/stuff/__init__.py         0      0   100%
build-install/usr/lib/python3.11/site-packages/stuff/test_thing.py       4      0   100%
----------------------------------------------------------------------------------------
TOTAL                                                                    4      0   100%


========================================= 1 passed in 0.06s =========================================
```

The warnings show that coverage tried to parse `src/stuff/thing.pyx` but could
not parse the Cython code. Instead Cython's coverage plugin should have done
this I think but somehow Cython's coverage plugin did not pick this up. I think
that this is because it could not find the files.

## Problem with Cython's coverage plugin

I think that Cython's coverage plugin assumes that `stuff.pyx`, `stuff.c` and
`stuff.so` are all located together. That is the case for an inplace setuptools
build but not for a meson build.

This is the initial file tree before building anything:

```console
$ tree -I .git
.
├── clean.sh
├── coverage_meson.sh
├── coverage_setuptools.sh
├── meson.build
├── meson.options
├── pyproject.toml
├── README.rst
├── requirements.txt
├── setup.py
└── src
    └── stuff
        ├── __init__.py
        ├── meson.build
        ├── test_thing.py
        └── thing.pyx

2 directories, 13 files
```

This is the layout after building with setuptools in-place:

```console
$ python setup.py build_ext --inplace
...
$ tree -I .git
.
├── build
│   └── temp.linux-x86_64-cpython-311
│       └── src
│           └── stuff
│               └── thing.o
├── clean.sh
├── coverage_meson.sh
├── coverage_setuptools.sh
├── meson.build
├── meson.options
├── pyproject.toml
├── README.rst
├── requirements.txt
├── setup.py
└── src
    └── stuff
        ├── __init__.py
        ├── meson.build
        ├── test_thing.py
        ├── thing.c
        ├── thing.cpython-311-x86_64-linux-gnu.so
        └── thing.pyx

6 directories, 16 files
```

This is the layout after building with `spin`:

```console
$ spin build --clean -- -Dcoverage=true
...
$ tree -I .git
.
├── build
│   ├── build.ninja
│   ├── compile_commands.json
│   ├── meson-info
│   │   ├── intro-benchmarks.json
│   │   ├── intro-buildoptions.json
│   │   ├── intro-buildsystem_files.json
│   │   ├── intro-compilers.json
│   │   ├── intro-dependencies.json
│   │   ├── intro-installed.json
│   │   ├── intro-install_plan.json
│   │   ├── intro-machines.json
│   │   ├── intro-projectinfo.json
│   │   ├── intro-targets.json
│   │   ├── intro-tests.json
│   │   └── meson-info.json
│   ├── meson-logs
│   │   ├── install-log.txt
│   │   └── meson-log.txt
│   ├── meson-private
│   │   ├── build.dat
│   │   ├── cmd_line.txt
│   │   ├── coredata.dat
│   │   ├── install.dat
│   │   ├── meson_benchmark_setup.dat
│   │   ├── meson.lock
│   │   ├── meson_test_setup.dat
│   │   ├── pycompile.py
│   │   ├── python-3.11-installed.json
│   │   ├── sanitycheckc.c
│   │   └── sanitycheckc.exe
│   └── src
│       └── stuff
│           ├── thing.cpython-311-x86_64-linux-gnu.so
│           └── thing.cpython-311-x86_64-linux-gnu.so.p
│               ├── meson-generated_src_stuff_thing.pyx.c.o
│               └── src
│                   └── stuff
│                       ├── thing.pyx.c
│                       └── thing.pyx.c.dep
├── build-install
│   └── usr
│       └── lib
│           └── python3.11
│               └── site-packages
│                   └── stuff
│                       ├── __init__.py
│                       ├── __pycache__
│                       │   ├── __init__.cpython-311.pyc
│                       │   └── test_thing.cpython-311.pyc
│                       ├── test_thing.py
│                       └── thing.cpython-311-x86_64-linux-gnu.so
├── clean.sh
├── coverage_meson.sh
├── coverage_setuptools.sh
├── meson.build
├── meson.options
├── pyproject.toml
├── README.rst
├── requirements.txt
├── setup.py
└── src
    └── stuff
        ├── __init__.py
        ├── meson.build
        ├── test_thing.py
        └── thing.pyx

18 directories, 49 files
```

Note that there is a `build` directory and a `build-install` directory and both
are separate from the `src` directory. With `meson` all builds are out-of-place
like the `build` directory here. When you do `spin build` what happens is that
`spin` first asks `meson` to build all generated files in the `build` directory
and then asks `meson` to "install" the files into the `build-install`
directory. Then when running a command like `spin test` or `spin run pytest
...` what happens is that `spin` makes the directory available (using
`PYTHONPATH`?) as if the project had been installed.

The `thing.pyx.c` file is in the `build` directory as is one copy of the
`thing.*.so` extension module. The `build-install` directory does not contain
any Cython files (`.pyx`) or Cython-generated sources (`.c`) but only the built
extension modules (`.so`) and Python (`.py`) files. When we actually run the
tests and collect coverage measurement we use only the files in the
`build-install` directory.

When running `spin run pytest --cov-stuff --pyargs stuff` the generated
`.coverage` file does contain references to `thing.pyx`:

```console
$ hd .coverage | grep -C 3 pyx
00004ea0  72 65 6e 74 2f 61 63 74  69 76 65 2f 63 79 74 68  |rent/active/cyth|
00004eb0  6f 6e 5f 63 6f 76 65 72  61 67 65 5f 64 65 6d 6f  |on_coverage_demo|
00004ec0  2f 73 72 63 2f 73 74 75  66 66 2f 74 68 69 6e 67  |/src/stuff/thing|
00004ed0  2e 70 79 78 3c 03 03 00  7f 2f 68 6f 6d 65 2f 6f  |.pyx<..../home/o|
00004ee0  73 63 61 72 2f 63 75 72  72 65 6e 74 2f 61 63 74  |scar/current/act|
00004ef0  69 76 65 2f 63 79 74 68  6f 6e 5f 63 6f 76 65 72  |ive/cython_cover|
00004f00  61 67 65 5f 64 65 6d 6f  2f 74 68 69 6e 67 2e 70  |age_demo/thing.p|
--
00005ea0  72 65 6e 74 2f 61 63 74  69 76 65 2f 63 79 74 68  |rent/active/cyth|
00005eb0  6f 6e 5f 63 6f 76 65 72  61 67 65 5f 64 65 6d 6f  |on_coverage_demo|
00005ec0  2f 73 72 63 2f 73 74 75  66 66 2f 74 68 69 6e 67  |/src/stuff/thing|
00005ed0  2e 70 79 78 04 3d 03 7f  01 2f 68 6f 6d 65 2f 6f  |.pyx.=.../home/o|
00005ee0  73 63 61 72 2f 63 75 72  72 65 6e 74 2f 61 63 74  |scar/current/act|
00005ef0  69 76 65 2f 63 79 74 68  6f 6e 5f 63 6f 76 65 72  |ive/cython_cover|
00005f00  61 67 65 5f 64 65 6d 6f  2f 74 68 69 6e 67 2e 70  |age_demo/thing.p|
```

These are presumably generated by the tracing code that Cython added in
`thing.pyx.c`. However at coverage report collection time Cython's coverage
plugin does not manage to intercept these and tell `coverage` how to report
the measurement (I think...).
