#!/bin/bash

CUDAROOT=/usr/local/cuda/

module load gcc/7.4.0
# module load gcc/4.8.5

export PATH=./contrib/bin:${PATH}
export INCLUDE=./contrib/include:${INCLUDE}
export LD_LIBRARY_PATH=./contrib/lib64:./contrib/lib:${LD_LIBRARY_PATH}


# export PATH=${HOME}/.local/gcc-4.9.2/bin:${PATH}
# export INCLUDE=${HOME}/.local/gcc-4.9.2/include:${INCLUDE}
# export LD_LIBRARY_PATH=${HOME}/.local/gcc-4.9.2/lib64:${HOME}/.local/gcc-4.9.2/lib:${LD_LIBRARY_PATH}

module load cuda/10.2/10.2.89
module load nccl/2.6/2.6.4-1
module load cudnn/7.6/7.6.5

export PATH=$CUDAROOT/bin:$PATH
export LD_LIBRARY_PATH=$CUDAROOT/lib64:$LD_LIBRARY_PATH
export CFLAGS="-I$CUDAROOT/include $CFLAGS"
export CPATH=$CUDAROOT/include:$CPATH
export CUDA_HOME=$CUDAROOT
export CUDA_PATH=$CUDAROOT

export CPATH=$NCCL_ROOT/include:$CPATH
export LD_LIBRARY_PATH=$NCCL_ROOT/lib/:$CUDAROOT/lib64:$LD_LIBRARY_PATH
export LIBRARY_PATH=$NCCL_ROOT/lib/:$LIBRARY_PATH


export PATH=./tools/kaldi/src/featbin/:${PATH}
