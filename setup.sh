#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE:-$0}")" > /dev/null; pwd)"

module load gcc/7.4.0

# ------------- internal tools -------------------
export PATH=${SCRIPT_DIR}/utils/:${SCRIPT_DIR}/kaldi/src/featbin/:${PATH}


# ------------- external libraries -------------------
CONTRIB_DIR=${SCRIPT_DIR}/contrib
export PATH=${CONTRIB_DIR}/bin:${PATH}
export INCLUDE=${CONTRIB_DIR}/include:${INCLUDE}
export LD_LIBRARY_PATH=${CONTRIB_DIR}/lib64:${CONTRIB_DIR}/lib:${LD_LIBRARY_PATH}


# ------------- Kaldi -------------------
export KALDI_ROOT=${SCRIPT_DIR}/tools/kaldi

export PATH=${KALDI_ROOT}/src/featbin/:${PATH}
[ -f $KALDI_ROOT/tools/env.sh ] && . $KALDI_ROOT/tools/env.sh
export PATH=$KALDI_ROOT/egs/timit/s5/utils/:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/tools/irstlm/bin/:$PWD:$PATH
[ ! -f $KALDI_ROOT/tools/config/common_path.sh ] && echo >&2 "The standard 
file $KALDI_ROOT/tools/config/common_path.sh is not present -> Exit!" && exit 1
. $KALDI_ROOT/tools/config/common_path.sh

export PATH=$PATH:$KALDI_ROOT/tools/openfst
export PATH=$PATH:$KALDI_ROOT/src/featbin
export PATH=$PATH:$KALDI_ROOT/src/gmmbin
export PATH=$PATH:$KALDI_ROOT/src/bin
export PATH=$PATH:$KALDI_ROOT//src/nnetbin

export LC_ALL=C
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/$KALDI_ROOT/src/lib:$KALDI_ROOT/tools/openfst-1.6.7/lib

export LD_LIBRARY_PATH=$KALDI_ROOT/tools/OpenBLAS/:$LD_LIBRARY_PATH


# ------------- CUDA ----------------
module load cuda/10.0/10.0.130
module load nccl/2.6/2.6.4-1
module load cudnn/7.6/7.6.5

export CUDAROOT=${CUDA_HOME}
export PATH=${CUDAROOT}/bin:${PATH}
export LD_LIBRARY_PATH=${CUDAROOT}/lib64:${LD_LIBRARY_PATH}
export CFLAGS="-I$CUDAROOT/include $CFLAGS"
export CPATH=${CUDAROOT}/include:${CPATH}
export CUDA_HOME=${CUDAROOT}
export CUDA_PATH=${CUDAROOT}

export NCCL_ROOT=${NCCL_HOME}
export CPATH=${NCCL_ROOT}/include:${CPATH}
export LD_LIBRARY_PATH=${NCCL_ROOT}/lib/:${CUDAROOT}/lib64:${LD_LIBRARY_PATH}
export LIBRARY_PATH=${NCCL_ROOT}/lib/:${LIBRARY_PATH}
