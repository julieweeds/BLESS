Basic usage of blesseval.py for running BLESS evaluations of thesauruses
Julie Weeds, July 2013

blesseval.py requires two input files (as well as the BLESS.txt file which is found in BLESS/data) per thesaurus which are neighbours.strings (a Byblo style neighbours file) and entries.totals.
entries.totals can be a Byblo style events.strings file (which has event frequency on each line) or (if correlation is required) be of the form event frequency width

The directory containing these two files (called neighbours.strings and events.totals) must be included in the conf.py file as parameters["thesdir"]

Basic use (which will output boxplots based on rank, similarities and "similarities as ranks") can then be achieved by running

python blesseval.py

Subsequent runs (with the same thesaurus) will be much faster if you run

python blesseval.py blesscache

If you require similarity scores to be normalised then run

python blesseval.py normalise

Arguments can be supplied in any order so you can also run
python blesseval.py blesscache normalise
python blesseval.py normalise blesscache

If entries.total has 3 fields per line (i.e., entry freq width) then it is possible to use the "correlate" option (to analyse correlations) and/or "predict_params" option (which analyses correlation and predicts normal distribution params based on width)
