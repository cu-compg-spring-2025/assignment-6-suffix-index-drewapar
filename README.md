[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2H4hMYgM)
# testSuffix
Testing suffix data structures for aligning reads to a reference.

## testSuffix
### Usage
```
usage: testSuffix.py [-h] [--reference REFERENCE] [--string STRING] --query_range QUERY_RANGE QUERY_RANGE QUERY_RANGE --out_file OUT_FILE

optional arguments:
  -h, --help     show this help message and exit
  --reference REFERENCE                                 Reference sequence file
  --string STRING                                       Reference string
  --query_range QUERY_RANGE QUERY_RANGE QUERY_RANGE     Query size range (start stop step)
  --out_file OUT_FILE                                   File to output results to
```
### Example
```
$ python testSuffix.py \
        --reference data/chr22.fa.gz \
        --query_range 5 50 5 \
        --out_file doc/suffix.png
```

<center><img src="/doc/suffix.png" width="600"/></center>