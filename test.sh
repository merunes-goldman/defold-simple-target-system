#!/bin/bash

source venv/bin/activate\
&& venv/bin/poetry run pytest tests
