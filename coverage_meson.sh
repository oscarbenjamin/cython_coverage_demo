#!/bin/bash

spin build --clean -- -Dcoverage=true
spin run pytest --cov=stuff --pyargs stuff
