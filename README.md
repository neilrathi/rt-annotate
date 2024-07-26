# rt-annotate

a super short python script to automatically annotate (reading time) datasets with common metrics used for mixed effects models, because i spend an annoying amount of time re-doing this entire process whenever i do reading time work.

## todo
- [ ] cli / refactor / cleanup / docs
- [ ] clean up dependency stuff
- [ ] add hdmi
- [ ] add surprisals ??

## dependencies
* [stanza](https://stanfordnlp.github.io/stanza/). the first time you run the script, models will be downloaded your home directory.
* [wordfreq](https://pypi.org/project/wordfreq/) for frequency estimation
* pandas