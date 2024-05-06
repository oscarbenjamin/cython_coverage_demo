#!/bin/bash

python setup.py build_ext --inplace
PYTHONPATH=src pytest --cov=stuff --pyargs stuff
