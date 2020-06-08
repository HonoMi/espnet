#!/bin/bash

source ./setup.sh

install_dir=`readlink -f ./contrib`
src_dir=./contrib/src

mkdir -p ${install_dir} 1>/dev/null 2>&1
mkdir -p ${src_dir} 1>/dev/null 2>&1

pushd ${src_dir}
    if [ ! -e flac-1.3.3.tar.xz ]; then
        wget https://downloads.xiph.org/releases/flac/flac-1.3.3.tar.xz
    fi
    if [ -e flac-1.3.3 ]; then
        rm -rf flac-1.3.3
    fi
    tar Jxfv ./flac-1.3.3.tar.xz

    cd flac-1.3.3
    ./configure --prefix=${install_dir} --disable-thorough-tests
    make
    make install
popd
