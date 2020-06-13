#!/usr/bin/env python3

# Copyright 2017 Hitachi.ltd (Terufumi.Morishita)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys
import os
from espnet.transformers.tokenizers import (
    load as load_transformer_tokenizer,
    tokenize as transformer_tokenize,
    is_subword_token as is_subword_token
)


is_python2 = sys.version_info[0] == 2


def get_parser():
    parser = argparse.ArgumentParser(
        description="convert raw text to tokenized text",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--output", required=True,
    )
    parser.add_argument(
        "--tokenizer_type", required=True
    )
    parser.add_argument(
        "--tokenizer_name_or_path",
        default=None,
        type=str,
        help="Optional pretrained tokenizer name or path if not the same as model_name_or_path. If both are None, initialize a new tokenizer.",
    )
    parser.add_argument(
        "--mecab_dic_dir",
        default=None,
    )
    parser.add_argument(
        "--cache_dir",
        default=None,
        type=str,
        help="Optional directory to store the pre-trained models downloaded from s3 (instead of the default one)",
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    args.tokenizer_type = args.tokenizer_type or None
    args.tokenizer_name_or_path = args.tokenizer_name_or_path or None
    transformer_tokenizer = load_transformer_tokenizer(
        args.tokenizer_type,
        name_or_path=args.tokenizer_name_or_path,
        mecab_dic_dir=args.mecab_dic_dir,
        cache_dir=args.cache_dir)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f_out:
        for word, id_ in sorted(transformer_tokenizer.get_vocab().items(),
                                key=lambda w_wid: w_wid[1]):
            print(word, id_, file=f_out)


if __name__ == "__main__":
    main()
