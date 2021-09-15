#!/bin/bash

python3 -m venv venv\
&& source venv/bin/activate\
&& venv/bin/python -m pip install --upgrade pip setuptools wheel\
&& venv/bin/pip install . --use-feature=in-tree-build
