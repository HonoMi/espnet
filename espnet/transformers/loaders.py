import logging

from transformers_extra.loaders import (
    load_config,
    # load_tokenizer
    load_model,
)
from .tokenizers import load as load_tokenizer

logger = logging.getLogger(__name__)


def load_all(task_type: str,
             model_type: str,
             config_name: str = None,
             model_name_or_path: str = None,
             tokenizer_type: str = None,
             tokenizer_name_or_path: str = None,
             cache_dir: str = None,
             mecab_dic_dir: str = None):

    config = load_config(model_type,
                         config_name=config_name,
                         name_or_path=model_name_or_path,
                         cache_dir=cache_dir)

    model = load_model(task_type,
                       model_type=model_type,
                       name_or_path=model_name_or_path,
                       config_name=config_name,
                       cache_dir=cache_dir)

    tokenizer = load_tokenizer(tokenizer_type or model_type,
                               name_or_path=tokenizer_name_or_path or model_name_or_path,
                               mecab_dic_dir=mecab_dic_dir,
                               cache_dir=cache_dir)

    if config.vocab_size != len(tokenizer):
        logger.warning(f'Vocab sizes differ between model and tokenizer ({config.vocab_size} != {len(tokenizer)}')
        # raise Exception(f'Vocab sizes differ between model and tokenizer ({config.vocab_size} != {len(tokenizer)}')

    return config, model, tokenizer
