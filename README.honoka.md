# espnet

## Installation
* 基本，公式に従えば良い．
* gcc=4.9.2 で実績あり．
    - 高すぎる(7.4.0)と，warpctcのビルドに失敗する．
    - 4.9.0以下はそもそも公式の要件を満たさない．
* [SeanNaren/warp-ctc](https://github.com/SeanNaren/warp-ctc)のインストール
    - CMakeLists.txt中の` --std=c++14`を` --std=c++11`に変えてからビルドすること．

## Entry Points
* `./egs/librispeech/asr1/run.sh`
* `./espnet/bin/lm_train.py`

