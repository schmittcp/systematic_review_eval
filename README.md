# NIST 2018 Systematic Review Evaluation code

This project contains code to evaluate the results of the 2018 NIST
Systematic Review challenge.


## To install: 
Clone this repository from github. Create a virtual environment and install required packages listed in requirements.txt.  The existing code was developed and tested on python 3.7.0.  

## Test cases:  
Unit test cases are in ./tests under testfiles. To run, run ./tests/rununittests.sh.  These
should complete successfully for all tests.


## To run: main code is in evaluation.py.  See runtest for example command line.
   usage: evaluation.py [-h] --gold_dir GOLD 
   	  		     --guess_dir GUESS 
			     --res_file RESFILE
                     	     --threshold THRESHOLD

   where gold_dir is directory holding human annotations
         guess_dir is directory holding machine annotations
         res_file is file to output results to
         threshold is the overlap (0.1 for low overlap to 1.0 for full overlap) for a hit to be called.

## Evaluation description:

The code looks for all annotation files in the gold directory.  It then looks for 
annotations files with the same names in the guess directory.  For each match, the
code compares the two annotations assuming the gold annotation represents the 
annotations. For each pair of files, the code compares mentions and groups independently.

### Mention annotations:

Comparing two annotation files - mentions:  Given a set of mentions Mgold from a
gold annotation file and a set of mentions Mguess from the guess annotation file,
the code takes each mention mi in Mgold and finds mentions mjs in Mguess that
have an overlap greater than the user provided threshold and where the type of
annotations match (e.g., Species annotation matches a species annotation).  

This essentially creates  a bipartite graph in which a mi may be assigned 
to more than one mj (and vice versa).
To create unique assignments, the python linear sum assignment from scipy.optmize
algorithm is used.  

Given unique assignments, the code then computes overall 
true positive, false positive, and false negatives for each
file, for each mention type, and overall.  Results are reported for
all annotations and by annotation type.

### Group annotations:

TBD

