import stanza
from wordfreq import word_frequency

import pandas as pd

dep_parser = stanza.Pipeline('en', processors='depparse,pos,mwt,tokenize,lemma')

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

df = pd.read_csv('example.csv')

# this feels messy
sentences = df.groupby('sent_num')['word'].apply(lambda x: ' '.join(x)).str[:-1].tolist()
df['dep_len'], df['integration_cost'] = dependency_length(sentences)

df['freq'] = df['word'].apply(lambda x: word_frequency(x, 'en'))
df['length'] = df['word'].apply(lambda x: len(x))

def lag(df, keys = ['freq', 'length'], num=2):

    for key in keys:
        for i in range(num):

            df[f'{key}_{i+1}'] = df.groupby('sent_num')[key].shift(i + 1)

    return df

df = lag(df)
df.to_csv('annotated.csv')