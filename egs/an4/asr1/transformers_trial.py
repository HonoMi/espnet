import click
from typing import List
import torch
# from transformers import *
# import transformers
from transformers import (
    GPT2Model, GPT2Tokenizer,
    BertModel, BertTokenizer
)

# # Transformers has a unified API
# # for 10 transformer architectures and 30 pretrained weights.
# #          Model          | Tokenizer          | Pretrained weights shortcut
# MODELS = [(BertModel,       BertTokenizer,       'bert-base-uncased'),
#           (OpenAIGPTModel,  OpenAIGPTTokenizer,  'openai-gpt'),
#           (GPT2Model,       GPT2Tokenizer,       'gpt2'),
#           (CTRLModel,       CTRLTokenizer,       'ctrl'),
#           (TransfoXLModel,  TransfoXLTokenizer,  'transfo-xl-wt103'),
#           (XLNetModel,      XLNetTokenizer,      'xlnet-base-cased'),
#           (XLMModel,        XLMTokenizer,        'xlm-mlm-enfr-1024'),
#           (DistilBertModel, DistilBertTokenizer, 'distilbert-base-cased'),
#           (RobertaModel,    RobertaTokenizer,    'roberta-base'),
#           (XLMRobertaModel, XLMRobertaTokenizer, 'xlm-roberta-base'),
#          ]


def tokenize(text: str,
             tokenizer,
             add_space_tokens=False):
    tokens = []
    for transformer_token in tokenizer.tokenize(text):
        if add_space_tokens and transformer_token.startswith('Ġ'):
            tokens.append('<space>')
            tokens.append(transformer_token)
        else:
            tokens.append(transformer_token)
    return tokens


def encode(tokens: List[str],
           tokenizer,
           add_special_tokens: bool = True) -> List[int]:
    return tokenizer.encode(tokens, add_special_tokens=add_special_tokens)


@click.command()
@click.option('--model', default='gpt', type=click.Choice(['gpt', 'bert']))
def main(model):

    if model == 'gpt':
        model = GPT2Model.from_pretrained('gpt2')
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    elif model == 'bert':
        model = BertModel.from_pretrained('bert-base-uncased')
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    token2id = tokenizer.get_vocab()
    id2token = {value: key for key, value in token2id.items()}
    text = 'Here is some text to encode.'

    def print_tokens(token_ids: List[int]):
        print(token_ids)
        for token_id in token_ids:
            print(token_id, id2token[token_id])

    tokens = tokenize(text, tokenizer)
    print('\n == tokens ==')
    print(tokens)

    # TODO: <space>
    print('\n== encode(tokens, add_special_tokens=True)')
    print_tokens(encode(tokens, tokenizer, add_special_tokens=True))

    print('\n== encode(tokens, add_special_tokens=False)')
    print_tokens(encode(tokens, tokenizer, add_special_tokens=False))

    print('\n== tokenizer.encode(text, add_special_tokens=True)')
    print_tokens(tokenizer.encode(text, add_special_tokens=True))

    print('\n== tokenizer.encode(text, add_special_tokens=False)')
    print_tokens(tokenizer.encode(text, add_special_tokens=False))

    # import pudb; pudb.set_trace()
    #
    # # Encode text
    # input_ids = torch.tensor([tokenizer.encode("Here is some text to encode", add_special_tokens=True)])  # Add special tokens takes care of adding [CLS], [SEP], <s>... tokens in the right way for each model.
    # with torch.no_grad():
    #     last_hidden_states = model(input_ids)[0]  # Models outputs are now tuples

if __name__ == '__main__':
    main()
