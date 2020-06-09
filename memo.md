# todo
* paste-feats
* まずan4で動かしてみる．
    - いや，librispeechだとbpeになっている．そこに違いがある．
* huggungfaceのdictを読み込ませることができるか．
    - まず，動かしてみて，dictの形式を見てみる．
* LM_interfaceの実装
* transformers_trial.pyをtransformers-extraに移動する．

## 変更点
* dict/data.jsonsの作成
* lm training

## 鬼門
* huggingfaceのvocabを，espnet側が読めるか
* huggingfaceのvocabが，フィラーなどを包含しているか．していないなら，vocabを作り直して学習し直さなければならない．
* <space> -> subword

## installation
* make check_install は通っていない．しかし，CUDA driverの違いなので，自分ではどうすることもできない．
```
Package cudatoolkit conflicts for:
pytorch=1.0.1 -> cudatoolkit[version='>=10.0,<10.1|>=9.0,<9.1|>=8.0,<8.1|>=9.2,<9.3.0a0|>=8.0,<8.1.0a0|>=10.0.130,<10.1.0a0|>=9.0,<9.1.0a0']
pytorch=1.0.1 -> cudnn[version='>=7.3.1,<8.0a0'] -> cudatoolkit[version='10.0.*|9.0.*|>=10.1,<10.2|>=9.2,<9.3|>=10.2,<10.3|9.2.*|8.0.*']The following specifications were found to be incompatible with your CUDA driver:

  - feature:/linux-64::__cuda==10.2=0
  -   - feature:|@/linux-64::__cuda==10.2=0
  -
  -   Your installed CUDA driver is: 10.2
  -
```



## an4
* **<space>も込みで言語モデルが学習されている．**
* <space>をどうするか．
* special tokenをどうするか．
* <space>もtoken_idになっている．これは，どう扱えばよいのか．lmの系列としても学習すべきか．
    - 理想
        * AMはspaceも学習する．
        * LMは，spaceは単に逆変換のために存在する．
    - おそらく，<space>も入れている



## <space>の方針
* ours
    - LMの学習では<space>は使わない．書き言葉からの転移を最大限に活かすため．
    - 音声認識のデコード時には，<space>に対応するidをスキップしながらスコアを出す．
* an4
    - text2tokens.py で，<space>を付与している．
    - <space>も込みでLMが学習されている．
    - おそらく，LMが受け取る入力中には，<space>に対応するidが含まれている．
