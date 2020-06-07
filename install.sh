#!/bin/bash

source ./setup.sh
conda install cmake
conda install -c conda-forge sox
conda install -c conda-forge ffmpeg

install_dir=`pwd -r`/contrib
src_dir=`pwd -r`/contrib/src
doc_dir=`pwd -r`/contrib/doc

mkdir -p ${install_dir} 1>/dev/null 2>&1
mkdir -p ${src_dir} 1>/dev/null 2>&1
mkdir -p ${doc_dir} 1>/dev/null 2>&1

pushd ${src_dir}
    if [ ! -e flac-1.3.3.tar.xz ]; then
        wget https://downloads.xiph.org/releases/flac/flac-1.3.3.tar.xz
    fi
    if [ -e flac-1.3.3 ]; then
        rm -rf flac-1.3.3
    fi
    tar Jxfv ./flac-1.3.3.tar.xz
    ./configure --prefix=${install_dir} --disable-thorough-tests
    make
    make install

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
