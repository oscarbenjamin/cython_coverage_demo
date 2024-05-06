#!/bin/bash

spin build --clean -- -Dcoverage=true

# Patch the .c file and rebuild:
git apply cfile.patch
spin build

spin run pytest --cov=stuff --pyargs stuff
