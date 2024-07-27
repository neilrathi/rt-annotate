import argparse
import numpy as np
import pandas as pd

import stanza
from wordfreq import word_frequency
from surprisal import AutoHuggingFaceModel

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, help='what to annotate', default = 'example.csv')
parser.add_argument('--nopunct', help='does your file not include punctuation?', action = 'store_true')
parser.add_argument('--depparse', help='compute dependency length?', action = 'store_true')
parser.add_argument('--surprisal', help='compute surprisals?', action = 'store_true')
parser.add_argument('--surp_model', type=str, help='huggingface surprisal model', default = 'gpt2')
parser.add_argument('--lag_num', type=int, help='how much lag', default = 2)
parser.add_argument('--lag_keys', type=list, help='which keys to lag', default = ['freq', 'length'])
args = parser.parse_args()

df = pd.read_csv(args.file)
if args.nopunct:
    sentences = df.groupby('sent_num')['word'].apply(lambda x: ' '.join(x)).str[:-1].tolist()
else:
    sentences = df.groupby('sent_num')['word'].apply(lambda x: ' '.join(x)).tolist()

def dependency_length(sentences):

    parsed = dep_parser(stanza.Document([], text=sentences))

    dep_lens = []
    integration_costs = []    

    for sent in parsed.sentences:

        discourse_refs = []

        for word in sent.words:

            dep_lens.append(max(0, word.id - word.head))

            if word.upos in ['NOUN', 'VERB']:
                discourse_refs.append(1)

            else:
                discourse_refs.append(0)

            integration_costs.append(sum(discourse_refs[(word.head - 1):(word.id - 1)]))

    return dep_lens, integration_costs

# this feels messy
if args.depparse:

    print('loading and computing dependency length...')
    dep_parser = stanza.Pipeline('en', processors='depparse,pos,mwt,tokenize,lemma', verbose=False)
    df['dep_len'], df['integration_cost'] = dependency_length(sentences)

# so does this but less so
if args.surprisal:

    print('loading and computing surprisals...')
    surprisal_model = AutoHuggingFaceModel.from_pretrained(args.surp_model)
    surprisals = []

    for i, s in enumerate(surprisal_model.surprise(sentences)):
        surprisals += list(s.surprisals[:len(sentences[i].split(' '))])

    df['surprisal'] = surprisals

df['freq'] = df['word'].apply(lambda x: word_frequency(x, 'en'))
df['length'] = df['word'].apply(lambda x: len(x))

def lag(df, keys = ['freq', 'length'], num=2):

    for key in keys:
        for i in range(num):

            df[f'{key}_{i+1}'] = df.groupby('sent_num')[key].shift(i + 1)

    return df

df = lag(df, keys = args.lag_keys, num = args.lag_num)
df.to_csv(args.file.split('.')[0] + '-annotated.csv')
print('done!')
