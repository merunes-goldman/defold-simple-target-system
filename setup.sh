#!/bin/bash

python3 -m venv venv\
&& source venv/bin/activate\
&& venv/bin/python -m pip install --upgrade pip poetry\
&& venv/bin/poetry install
