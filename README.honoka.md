# espnet

## Installation
1. virtual envを用意する．
    ```sh
    pyenv virtualenv anaconda3-5.3.1 espnet
    pyenv local espnet
    ```
1. 環境変数の設定などを行う．
    ```sh
    source ./setup.sh
    ```
1. 公式に従って，espnetとその依存モジュールをインストールする．ただし，espnetのインストールの時には，`using the system Python without creating new python environment`に従うこと．
    - インストールスクリプト `./インストール_scripts/インストール_all.sh` を作った．動くかもしれない．
1. 追加のpythonモジュールをインストールする．
    ```sh
    pip install -r requirements.txt
    ```


以下，ポイント．
* gcc=4.9.2 で実績あり．
    - 高すぎる(7.4.0)と，warpctcのビルドに失敗する．
    - 4.9.0以下はそもそも公式の要件を満たさない．
* [SeanNaren/warp-ctc](https://github.com/SeanNaren/warp-ctc)のインストールは，CMakeLists.txt中の` --std=c++14`を` --std=c++11`に変えてからビルドすること．
* flacは[ここ](http://www.linuxfromscratch.org/blfs/view/svn/multimedia/flac.html)からインストールする．
* libsndは[ここ](http://lfsbookja.osdn.jp/BLFS/svn-ja/multimedia/libsndfile.html)からインストールする．

## Docs
* [Usage - ESPnet](https://espnet.github.io/espnet/tutorial.html)

## Entry Points
* `./egs/an4/asr1`
* `./egs/librispeech/asr1/run.sh`
* `./espnet/bin/lm_train.py`

