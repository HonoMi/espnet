#!/bin/bash

STAGE=1
STOP_STAGE=2
LOG=./log.txt
QSUB_LOG=./log.qsub.txt
QSUB_ERR=./err.qsub.txt

cmd="\
source ../../../setup.sh;\
./run.sh --stage ${STAGE} --stop-stage ${STOP_STAGE} --ngpu 4 1>${LOG} 2>&1"


launch-qsub\
    "${cmd}"\
    "ABCI"\
    "rt_G.large"\
    -e ${QSUB_ERR}\
    -o ${QSUB_LOG}
