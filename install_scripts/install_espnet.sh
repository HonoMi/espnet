#!/bin/bash

cd tools
rm -rf venv; mkdir -p venv/bin; touch venv/bin/activate
make KALDI=./kaldi CUDA_VERSION=10.2 PYTHON=dummy
