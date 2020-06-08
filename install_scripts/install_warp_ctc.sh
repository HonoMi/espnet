#!/bin/bash

source ./setup.sh
install_dir=`readlink -f ./contrib`
src_dir=./contrib/src

pushd ${src_dir}
    if [ ! -e warp-ctc ]; then
        git clone https://github.com/SeanNaren/warp-ctc
    fi
    cd warp-ctc

    sed 's:c++14:c++11:g' -i CMakeLists.txt

    mkdir build
    cd build
    cmake ..
    make

    cd ../pytorch_binding
    python setup.py install

popd
