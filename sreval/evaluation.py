"""

This module is used to compare the results of a set of gold standard
annotations against a set of machine generated annotations.  Annotations
in both cases are instances of brat_dm data models.


"""
import argparse
import os
from brat_dm import BratDataModel
import numpy as np
from scipy.optimize import linear_sum_assignment
import traceback
from srresult import SRResult
from sr_comparator_mentions import compare_mentions
from sr_comparator_groups import compare_groups
from sr_comparator_mentions import get_mention_mappings



def compare_dirs(gold_dir, guess_dir):
    """ Compares the files in the two directories using compare_files
    :param gold_dir: director holding gold results
    :param guess_dir: director holding guess results
    :return list of list, each sublist being a matching pair of gold and guess results
    """
    # get files in the gold directory
    to_skip = set()
    gold_bdms = {}
    for annfile in os.listdir(gold_dir):
        if annfile.endswith('.xml'):
            try:
                gold_bdms[annfile] = BratDataModel()
                gold_bdms[annfile].addannotations(os.path.join(gold_dir, annfile))
            except:
                print("Fail to parse gold "+str(os.path.join(gold_dir,annfile))+", skipping")
                print(traceback.format_exc())
                to_skip.add(annfile)

    # get matching models from the model directory
    guess_bdms = {}
    for annfile in os.listdir(guess_dir):
        if annfile in gold_bdms:
            if annfile not in to_skip:
                guess_bdms[annfile] = BratDataModel()
                guess_bdms[annfile].addannotations(os.path.join(guess_dir, annfile))

    # check same number of results
    if len(gold_bdms) != len(guess_bdms):
        for item in set(gold_bdms.keys()) - set(guess_bdms.keys()):
              print(" skipped file "+str(item))
        raise ValueError("Annotation files in guess directories do not include all files in the golden directory")

    res=[]
    for key in gold_bdms:
        res.append([gold_bdms[key], guess_bdms[key]])

    if (len(to_skip))>0:
        print("Warning: number of skipped files "+len(to_skip))
        for item in to_skip:
              print(" skipped file "+str(item))
    return res




def main():
    parser = argparse.ArgumentParser(description='Evaluate TAC 2018 Systematic Review Methods')
    parser.add_argument('--gold_dir', metavar='GOLD', required=True, type=str, help='path to directory containing human curated data')
    parser.add_argument('--guess_dir', metavar='GUESS', required=True, type=str, help='path to directory containing model generated data')
    parser.add_argument('--res_file', metavar='RESFILE', required=True, type=str, help='filenane to write results to')
    parser.add_argument('--mention_threshold', metavar='MENTION_THRESHOLD', required=True, type=float, help='threshold for mention classification (0-1)')
    parser.add_argument('--group_threshold', metavar='GROUP_THRESHOLD', required=False, type=float, help='threshold for group classification (0-1)')
    args = parser.parse_args()

    with open(args.res_file, 'w') as out_file:
        out_file.write('Results\n')
        out_file.write("Gold directory "+args.gold_dir+"\n")
        out_file.write("Guess directory " + args.guess_dir + "\n")
        out_file.write("Mention threshold " + str(args.mention_threshold) + "\n")

        if args.group_threshold is None:
            args.group_threshold=args.mention_threshold
        out_file.write("Group threshold " + str(args.group_threshold) + "\n")

        bdmslist = compare_dirs(args.gold_dir, args.guess_dir)

        mresmap = compare_mentions(bdmslist, args.mention_threshold)
        mtypes=sorted(list(mresmap.keys()))
        for mtype in mtypes:
            out_file.write("Mention results for type " + str(mtype) + " is\t\t" + str(mresmap[mtype])+"\n")

        comlist = get_mention_mappings(bdmslist, args.mention_threshold)
        gresmap = compare_groups(comlist, args.group_threshold)
        mtypes=sorted(list(gresmap.keys()))
        for mtype in mtypes:
            out_file.write("Group results for type " + str(mtype) + " is\t\t" + str(gresmap[mtype])+"\n")



if __name__ == "__main__":
    main()






