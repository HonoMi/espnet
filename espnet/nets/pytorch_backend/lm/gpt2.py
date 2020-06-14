from typing import Any
from typing import List
from typing import Tuple

import torch

from espnet.nets.lm_interface import LMInterface

from espnet.transformers import loaders
from espnet.transformers import tokenizers
from espnet.nets.scorer_interface import BatchScorerInterface


class GPT2(BatchScorerInterface, LMInterface, torch.nn.Module):
    """Sequential RNNLM.

    See also:
        https://github.com/pytorch/examples/blob/4581968193699de14b56527296262dd76ab43557/word_language_model/model.py

    """

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("--transformers-model-type", default='gpt2')
        parser.add_argument("--transformers-model-name-or-path", default='gpt2')
        parser.add_argument("--transformers-tokenizer-type", default=None)
        parser.add_argument("--transformers-tokenizer-name-or-path", default=None)
        parser.add_argument("--no-skip-space-tokens", default=True)
        parser.add_argument("--space-token", default='<space>')
        return parser

    def __init__(self, n_vocab, args):
        """Initialize class.

        Args:
            n_vocab (int): The size of the vocabulary
            args (argparse.Namespace): configurations. see py:method:`add_arguments`

        """
        torch.nn.Module.__init__(self)

        _, model, tokenizer = loaders.load_all(
            'language_modeling',
            args.transformers_model_type,
            model_name_or_path=args.transformers_model_name_or_path,
            tokenizer_type=args.transformers_tokenizer_type or args.transformers_model_type,
            tokenizer_name_or_path=args.transformers_tokenizer_name_or_path or args.transformers_model_name_or_path,
        )
        
        self._model = model
        self._tokenizer = tokenizer

        self._no_skip_space_tokens = args.no_skip_space_tokens
        self._space_token_id = self._tokenizer.get_vocab()[args.space_token]

    def forward(self, x, t):
        """Compute LM loss value from buffer sequences.

        Args:
            x (torch.Tensor): Input ids. (batch, len)
            t (torch.Tensor): Target ids. (batch, len)

        Returns:
            tuple[torch.Tensor, torch.Tensor, torch.Tensor]: Tuple of
                loss to backward (scalar),
                negative log-likelihood of t: -log p(t) (scalar) and
                the number of elements in x (scalar)

        Notes:
            The last two return values are used
            in perplexity: p(t)^{-n} = exp(-log p(t) / n)

        """
        """espnet
            x:
                tensor([[50261,    48,   441,  ...,   400,   310,  1169],
                        [50261,  3526,  1138,  ...,  9937,   312, 10427],
                        [50261, 34552,  3526,  ...,    57,   312, 10427],
                        ...,
                        [50261,    33,   338,  ...,     0,     0,     0],
                        [50261,    34,   413,  ...,     0,     0,     0],
                        [50261, 11652,   377,  ...,     0,     0,     0]], device='cuda:0')
            t:
                tensor([[   48,   441,   338,  ...,   310,  1169, 50261],
                        [ 3526,  1138,   377,  ...,   312, 10427, 50261],
                        [34552,  3526,    57,  ...,   312, 10427, 50261],
                        ...,
                        [   33,   338,   351,  ...,  -100,  -100,  -100],
                        [   34,   413,   318,  ...,  -100,  -100,  -100],
                        [11652,   377,  9307,  ...,  -100,  -100,  -100]], device='cuda:0')
            >> y = self._before_loss(x, None)[0]
            >> mask = (x != 0).to(y.dtype)
            >> loss = F.cross_entropy(y.view(-1, y.shape[-1]), t.view(-1), reduction="none")
            >> logp = loss * mask.view(-1)
            >> logp = logp.sum()
            >> count = mask.sum()
            >> return logp / count, logp, count
        """
        """transformers.examples.run_language_modeling.py
            inputs:
                tensor([[ 4840,  7153, 16247,  ...,     2,     2,     2],
                        [25986, 15275, 16403,  ...,     2,     2,     2],
                        [ 2857,  2889,  2919,  ...,     2,     2,     2],
                        ...,
                        [19330, 15488, 17132,  ...,     2,     2,     2],
                        [25233, 15636, 16575,  ...,     2,     2,     2],
                        [10056,  3377, 15536,  ..., 15305, 11913, 15240]])
            labels:
                tensor([[ 4840,  7153, 16247,  ...,     2,     2,     2],
                        [25986, 15275, 16403,  ...,     2,     2,     2],
                        [ 2857,  2889,  2919,  ...,     2,     2,     2],
                        ...,
                        [19330, 15488, 17132,  ...,     2,     2,     2],
                        [25233, 15636, 16575,  ...,     2,     2,     2],
                        [10056,  3377, 15536,  ..., 15305, 11913, 15240]])

            >> inputs, labels = mask_tokens(batch, tokenizer, args.mlm_probability) if args.mlm else (batch, batch)
            >> inputs = inputs.to(args.device)
            >> labels = labels.to(args.device)

            >> model.train()
            >> outputs = model(inputs, masked_lm_labels=labels) if args.mlm else model(inputs, labels=labels)
            >> loss = outputs[0]  # model outputs are always tuple in transformers (see doc)
        """
        """espnetとtransformersの差分
            1. labelの与え方．
                - espnet: tはxを１つ右にシフト
                - transformers: シフト無し．(tはxと完全に等しい)
            2. paddingの与え方
                - espnet: xは0, tは-100
                - transformers: 以下．
                    def collate(examples: List[torch.Tensor]):
                        if tokenizer._pad_token is None:
                            return pad_sequence(examples, batch_first=True)
                        return pad_sequence(examples, batch_first=True, padding_value=tokenizer.pad_token_id)

            3. <bos> <eos> の考え方
                - espnet: lm_train.py内で自動で追加される．
                    具体的には，espnet.lm.lm_utils.ParallelSentenceIteratorが自動で追加する．具体的には，xの文頭に文頭記号を，tの文末に文末記号を，加える．
                    '<sos> w1 w2 w3' and 'w1 w2 w3 <eos>'
                - transformers: tokenizer.encodeが加える．
        """
        """方針
            1. labelの与え方
                - t==xに戻す．
            2. paddingの与え方
                tokenizer.pad_token_id に置き換える．
            3. <boe> <eos> の考え方
        """
        # TODO: 本当は，以下の操作は全て，gradientを切らないようにする必要がある．
        # しかし，x/tはグラフの最初であることが分かっているため，今は気にしていない．


        vocab = self._tokenizer.get_vocab()

        x_refer = x.clone().cpu().detach()
        space_token_id = vocab[tokenizers.ESPNET_SPACE_TOKEN]
        x_without_space_token = []
        for row in x_refer:
            row_without_space_token = []
            for val in row:
                if val == space_token_id:
                    continue
                row_without_space_token.append(val.numpy().tolist())
            x_without_space_token.append(row_without_space_token)

        inputs = torch.tensor(x_without_space_token, dtype=x.dtype).to(x.device)

        # TODO: マッピング機能を，tokenizersに移行する．
        # xの中に50261が入っている．これのせいでCUDA Error
        # model embed: 50257, vocab: 50260

        # -- mapping from espnet token ids to transformers token ids --

        def map_espnet_to_transfo(src_id: int, tgt_id: int):
            inputs[inputs == src_id] = tgt_id

        # padding token
        pad_token_id = self._tokenizer.pad_token_id or 0
        map_espnet_to_transfo(0, pad_token_id)

        # unk token
        map_espnet_to_transfo(vocab[tokenizers.ESPNET_UNK_TOKEN],
                              self._tokenizer.unk_token_id)

        # eos token
        map_espnet_to_transfo(vocab[tokenizers.ESPNET_EOS_TOKEN],
                              self._tokenizer.eos_token_id)

        labels = inputs.clone()
        outputs = self._model(inputs, labels=labels)
        loss = outputs[0]

        count = torch.sum(labels != pad_token_id)
        # TODO: return tuple

        # 50257

        return loss, loss * count, count


    # batch beam search API (see BatchScorerInterface)
    def batch_score(
        self, ys: torch.Tensor, states: List[Any], xs: torch.Tensor
    ) -> Tuple[torch.Tensor, List[Any]]:
        # """Score new token batch.
        # import pudb; pudb.set_trace()
        with open('out.txt', 'w') as f:
            print('xs', xs, file=f)  # real valued. トークンの確率？
            print('xs.shape', xs.shape, file=f)
            print('ys', ys, file=f)
            print('ys', ys.shape, file=f)

        # Args:
        #     ys (torch.Tensor): torch.int64 prefix tokens (n_batch, ylen).
        #     states (List[Any]): Scorer states for prefix tokens.
        #     xs (torch.Tensor):
        #         The encoder feature that generates ys (n_batch, xlen, n_feat).

        # Returns:
        #     tuple[torch.Tensor, List[Any]]: Tuple of
        #         batchfied scores for next token with shape of `(n_batch, n_vocab)`
        #         and next state list for ys.

        # """
        # # merge states
        # n_batch = len(ys)
        # n_layers = self.model.predictor.n_layers
        # if self.model.predictor.typ == "lstm":
        #     keys = ("c", "h")
        # else:
        #     keys = ("h",)

        # if states[0] is None:
        #     states = None
        # else:
        #     # transpose state of [batch, key, layer] into [key, layer, batch]
        #     states = {
        #         k: [
        #             torch.stack([states[b][k][i] for b in range(n_batch)])
        #             for i in range(n_layers)
        #         ]
        #         for k in keys
        #     }
        # states, logp = self.model.predict(states, ys[:, -1])

        # # transpose state of [key, layer, batch] into [batch, key, layer]
        # return (
        #     logp,
        #     [
        #         {k: [states[k][i][b] for i in range(n_layers)] for k in keys}
        #         for b in range(n_batch)
        #     ],
        # )
