import torch
from transformers import (
    GPT2Tokenizer,
)
from transformers_extra import loaders


ESPNET_PAD_IDs = [0, -100]    # lm.py: 140
ESPNET_UNK_TOKEN = '<unk>'    # lm_train.py: 260~
ESPNET_EOS_TOKEN = '<eos>'    # lm_train.py: 260~

ESPNET_SPACE_TOKEN = '<space>'
ESPNET_BLANK_TOKEN = '<blank>'    # lm_train.py: 260~


def map_token_id(espnet_id: int,
                 tokenizer):
    vocab = tokenizer.get_vocab()

    if espnet_id in ESPNET_PAD_IDs:
        if tokenizer.pad_token is not None:
            return tokenizer.pad_token_id
        else:
            return 0

    if espnet_id == vocab[ESPNET_UNK_TOKEN]:
        return tokenizer.unk_token_id

    if espnet_id == vocab[ESPNET_EOS_TOKEN]:
        return tokenizer.unk_token_id

    return espnet_id


def map_token_ids(espnet_ids: torch.Tensor,
                  tokenizer,
                  remove_space_tokens=False):

    vocab = tokenizer.get_vocab()

    x_refer = espnet_ids.clone().cpu().detach()
    space_token_id = vocab[ESPNET_SPACE_TOKEN]
    x_without_space_token = []
    for row in x_refer:
        row_without_space_token = []
        for val in row:
            if remove_space_tokens and val == space_token_id:
                continue
            row_without_space_token.append(val.numpy().tolist())
        x_without_space_token.append(row_without_space_token)

    inputs = torch.tensor(x_without_space_token,
                          dtype=espnet_ids.dtype)\
        .to(espnet_ids.device)

    def map_espnet_to_transfo(src_id: int, tgt_id: int):
        inputs[inputs == src_id] = tgt_id

    # padding token
    pad_token_id = tokenizer.pad_token_id or 0
    for espnet_pad_id in ESPNET_PAD_IDs:
        map_espnet_to_transfo(espnet_pad_id, pad_token_id)
        map_espnet_to_transfo(espnet_pad_id, pad_token_id)

    # unk token
    map_espnet_to_transfo(vocab[ESPNET_UNK_TOKEN],
                          tokenizer.unk_token_id)

    # eos token
    map_espnet_to_transfo(vocab[ESPNET_EOS_TOKEN],
                          tokenizer.eos_token_id)
    return inputs


def is_subword_token(token: str,
                     transformer_tokenizer):
    if isinstance(transformer_tokenizer, GPT2Tokenizer):
        # TODO: transformersに，is_subword_token()みたいな機能があれば，それを使う．
        return token.startswith('Ġ')
    else:
        raise Exception(f'Unknown class "{transformer_tokenizer.__class__.__name__}"')


def tokenize(text: str,
             transformer_tokenizer,
             space_token=ESPNET_SPACE_TOKEN,
             add_space_tokens=True):
    tokens = []
    for transformer_token in transformer_tokenizer.tokenize(text):
        if add_space_tokens and transformer_token.startswith('Ġ'):
            tokens.append(space_token)
            tokens.append(transformer_token)
        else:
            tokens.append(transformer_token)
    return tokens


def load(type_: str,
         name_or_path: str = None,
         mecab_dic_dir: str = None,
         cache_dir: str = None,
         space_token=ESPNET_SPACE_TOKEN,
         unk_token=ESPNET_UNK_TOKEN,
         eos_token=ESPNET_EOS_TOKEN,
         blank_token=ESPNET_BLANK_TOKEN):

    tokenizer = loaders.load_tokenizer(
        type_,
        name_or_path=name_or_path,
        mecab_dic_dir=mecab_dic_dir,
        cache_dir=cache_dir)

    tokenizer.add_tokens([
        space_token,
        unk_token,
        eos_token,
        blank_token,
    ])
    return tokenizer
