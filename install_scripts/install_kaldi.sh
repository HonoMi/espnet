#!/bin/bash

source ./setup.sh
NUM_CPU=20

# ./ci/install_kaldi.sh

cd tools
git clone https://github.com/kaldi-asr/kaldi

cd kaldi/tools
make -j
./extras/install_openblas.sh

cd ../src
./configure --openblas-root=../tools/OpenBLAS/install --use-cuda=no
make -j clean depend; make -j ${NUM_CPU}
