#!/bin/bash

install_dir=./contrib
src_dir=./contrib/src
doc_dir=./contrib/doc

mkdir -p ${install_dir} 1>/dev/null 2>&1
mkdir -p ${src_dir} 1>/dev/null 2>&1
mkdir -p ${doc_dir} 1>/dev/null 2>&1

pushd ${src_dir}
    if [ ! -e libsndfile-1.0.28.tar.gz ]; then
        wet http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.28.tar.gz
    fi
    if [ -e libsndfile-1.0.28 ]; then
        rm -rf libsndfile-1.0.28
    fi
    tar -zxvf  ./libsndfile-1.0.28.tar.gz
    ./configure --prefix=${install_dir} --disable-static --docdir=${doc_dir}
    make
    make install
popd
