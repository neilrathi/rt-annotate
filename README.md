# rt-annotate

a super short python script to automatically annotate (reading time) datasets with common metrics used in analysis

## docs
files NEED to have a column named `word`, and preferably a `sent_num` column (although this can optionally be generated via periods with the `--sentcol NONE` argument). nothing else is used.

to annotate a file with basic (lagged) frequency and length measures:
```bash
python3 parse.py --file my_file.csv
```

the optional `--depparse` and `--surprisal` flags compute dependency length / integration cost and surprisal, respectively. you can also lag any keys as many times as you want. for example, to annotate a file that has no punctuation with dependency and surprisal metrics in addition to frequency and length, with 3x lag for surprisal, frequency, and length:

```bash
python3 parse.py --file my_file.csv --nopunct --depparse --surprisal --lag_num 3 --lag_keys surprisal freq length
```

you can also choose which huggingface model to use for surprisal with `--surp_model`.

## dependencies
* [stanza](https://stanfordnlp.github.io/stanza/). the first time you run the script with `--depparse`, models will be downloaded your home directory.
* [surprisal](https://github.com/aalok-sathe/surprisal/) for surprisal. the first time you run the script with `--surprisal`, models will be downloaded your home directory.
* [wordfreq](https://pypi.org/project/wordfreq/) for frequency estimation
* pandas, numpy

## todo
- [ ] cli / refactor / cleanup / docs
- [ ] clean up dependency stuff
- [ ] add hdmi