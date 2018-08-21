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
                     	     --mention_threshold MENTION_THRESHOLD
                     	     --group_threshold GROUP_THRESHOLD
   where: 
   
   gold_dir is directory holding human annotations
   
   guess_dir is directory holding machine annotations
   
   res_file is file to output results to
   
   mention_threshold is the overlap (0.1 for low overlap to 1.0 for full overlap) for a hit to be called
     on two mention annotations.
     
   group_threshold is the overlap (0.1 for low overlap to 1.0 for full overlap) for a hit to be called
     on two mention annotations (defaults to mention_threshold value if not provided).
     

## Evaluation description:

The code looks for all annotation files in the gold directory.  It then looks for 
annotations files with the same names in the guess directory.  For each match, the
code compares the two annotation files assuming the gold annotation represents the 
correct annotations.  The code outputs results for all annotation types and for
each annotation type (e.g., results are provided for 'species', 'sex').

### Mention annotations:

Comparing two annotation files - mentions:  Given a set of mentions Mgold from a
gold annotation file and a set of mentions Mguess from the guess annotation file,
the code takes each mention mi in Mgold and finds mentions mjs in Mguess that
have an overlap greater than the user provided mention_threshold and where the type of
annotations match (e.g., Species annotation matches a species annotation).  

This creates a bipartite graph in which a mi may be assigned 
to more than one mj (and vice versa).
To create unique assignments, the python linear sum assignment from scipy.optmize
algorithm is used.  

Given unique assignments, the code then computes overall 
true positive, false positive, and false negatives for each
file, for each mention type, and overall.  Results are reported for
all annotations and by annotation type.

### Group annotations:

Comparing two annotation files - groups:  Given a set of group annotations GAgold from
a gold annotation file and a set of group annotations GAguess from the guess annotation file,
the code first collects the group annotations and creates group models.  A group model 
holds all the group annotations that are related, e.g., a group model will contain the test article
mention and the vehicle mention that are in the same test article group.  

A group model is created for each set of related group annotations, resulting in a set of 
gold group models, GMgold, and a set of estimated group models, GMguess.

The code then compares each gold group model, gomi, and each guessed group model gumj, to each 
other, calculating a similarity score.  The score is equal to 2 times the number of mention
annotations they have in common divided by the total number of mention annotations in the two
group models being compared.  This gives a score of 0 for no match to 1 for full match and a 
score of 0 is given if the score is less than the group_threshold.  Group
models of different group types are not compared.  Also, to be considered a common mention, the
mentions have to had been matched in the mention annotation matching process described above.

The scores generate a bipartite graph in which a gold group model may be assigned to more than 
one guess group model (and vice versa).  To create unique assignments, the python 
linear sum assignment from scipy.optmize algorithm is used.  

Given unique assignments, the code then computes overall true positive, false positive, and false negatives for each
file, for each group type, and overall.  





