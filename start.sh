#!/usr/bin/env bash
pip install Flask
pip install radon
pip install gitpython
pip install dask distributed
dask-scheduler
dask-worker 127.0.0.1:8786
dask-worker 127.0.0.1:8786
dask-worker 127.0.0.1:8786
python CodeComplexity.py
