"""

This module is used to compare the results of a set of gold standard
annotations against a set of machine generated annotations.  Annotations
in both cases are instances of brat_dm data models.

Example:
    asdfasdf


Todo:
    * write the darn thing
    * test the darn thing



"""
import argparse
import os
#from sreval.brat_dm import BratDataModel
from brat_dm import BratDataModel
import numpy as np
from scipy.optimize import linear_sum_assignment
import traceback

class SRClassification:
    """ Holds classification results of an algorithm """
    def __init__(self):
        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def precision(self):
        if self.tp == 0:
            return 0.0
        return 100. * self.tp / (self.tp + self.fp)

    def recall(self):
        if self.tp == 0:
            return 0.0
        return 100. * self.tp / (self.tp + self.fn)

    def f1(self):
        p, r = self.precision(), self.recall()
        if p + r == 0.0:
            return 0.0
        return 2 * p * r / (p + r)

    def __str__(self):
        return "Classification:\ttp\t"+str(self.tp)+"\tfp "+str(self.fp)+"\tfn "+str(self.fn)+"\tf1 "+str(self.f1())


class SRComparator:
    """ Compares sets of mentions (brat_dm) """

    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def compare(self, golddm, guessdm, res, mtype=None):
        """ compare gold results versus guess results on a single data set using exaction mention matching
        :param golddm gold BratDataModel instance
        :param guessdm guess BratDataModel instance
        :param res, classification instance holding results, to be updated by this method
        :param mtype, mention type to restrict results to, if none will process all types

        """
        if mtype is None:
            gold_list = [m for m in golddm.allmentions()]
            guess_list = [m for m in guessdm.allmentions()]
        else:
            gold_list = [m for m in golddm.mentions_by_types(mtype)]
            guess_list = [m for m in guessdm.mentions_by_types(mtype)]
        print("compare: type "+str(mtype)+", len gold mentions "+str(len(gold_list))+", len guess mentions "+str(len(guess_list)))

        guess_ind=get_assignments(guess_list,gold_list,1.0-self.threshold)

        """ now calculate the scores.  If a guess was assigned to a gold with a overlap score
            of 1.0, then there is no actual match for the guess (e.g., a false positive).  If 
            a guess has no match or if the match is below the overlap threshold, then score it
            as a false positive.  If a gold has no match above overlap threshold, then score 
            it as a false negative 
        """
        goldhit = [0]*len(gold_list)
        for guessi in range(0, len(guess_list)):
            if guess_ind[guessi]>=0:
                res.tp += 1
                goldhit[guess_ind[guessi]] = 1
            else:
                res.fp += 1

        for goldi in range(0, len(gold_list)):
            if goldhit[goldi] == 0:
                res.fn += 1

def get_assignments(guess_list, gold_list, cost_max):
    """ assign each element of guess_list to an element of gold_list
        such that guess are assigned preferentially to elements of gold
        that they have greater overlap with.
    :return list of size guess_list with assignment for each, if -1 then no assignment

        Fundamentally, this is a bipartite graph matching problem and there are varying ways of
        solving it.  We use the hungarian algorithm as it allows weighted matrix and the scipy
        implementation: scipy.optimize.linear_sum_assignment
    """

    # get cost matrix, should be square, set to large value (high cost) as default
    mhigh=10.0
    mlen=max(len(guess_list),len(gold_list))   
    mcost = mhigh*np.ones((mlen,mlen))
    print("mlen "+str(mlen))
    for guessi in range(0, len(guess_list)):
        for goldi in range(0, len(gold_list)):
                overlap = get_overlap(guess_list[guessi], gold_list[goldi])
                lengold = getsumdiffs(gold_list[goldi].malocs)
                lenguess = getsumdiffs(guess_list[guessi].malocs)
                mcost[guessi, goldi] = 1.0-(2.0*overlap/(lengold+lenguess))
                if mcost[guessi, goldi]>cost_max:
                    mcost[guessi, goldi]=mhigh
                print("get_assign "+str(overlap)+", guess locs "+str(guess_list[guessi].malocs)+", gold locs "+str(gold_list[goldi].malocs)+", goldsumdiffs "+str(lengold)+", guesssumdiffs "+str(lenguess))

    row_ind, col_ind = linear_sum_assignment(mcost)
    print("get_assign: cost "+str(mcost))
    print("get_assign: initial assign "+str(col_ind))

    retl=len(guess_list)*[-1]
    for i in range(0,len(retl)):
        if mcost[i,col_ind[i]]<mhigh:
            retl[i]=col_ind[i]
    print("get_assign: final assign "+str(retl))

    return retl


def getsumdiffs(l):
    """ l is list of list of x1,x2 pairs.  compute sum of x2-x1 """
    ret=0
    for li in l:
        ret += li[1]-li[0]
    return ret


def get_overlap(goldma, guessma):
    """ get the overlap between two mentions, zero if none or different types """
    if goldma.matype != guessma.matype:
        return 0
    overlap = 0
    for i in range(0, len(guessma.malocs)):
        for j in range(0, len(goldma.malocs)):
            to = get_seg_overlap(guessma.malocs[i],goldma.malocs[j])
            overlap += to
    return overlap

def get_seg_overlap(seg1, seg2):
    """ given two lists l1[i,j] and l2[k,l] return teh overlap,
        e.g., l1[2,5] and l2[4,6] has an overlap of 1 """
    if seg1[1] < seg2[0] or seg1[0] > seg2[1]:
        return 0
    return min(seg1[1], seg2[1])-max(seg1[0], seg2[0])


def compare_mention_list(reslist, srcomparator):
    """ compare gold results versus model results
    :param reslist list of list, each sublist being a matching pair of gold and guess BratDataModel results
    :param comparator, function that can compare two brat_dm instances and update a classification result
    """
    res=SRClassification()
    for i in range(0, len(reslist)):
        srcomparator.compare(reslist[i][0], reslist[i][1], res)
    return res


def compare_mention_list_by_type(reslist, srcomparator):
    """ compare gold results versus model results
    :param reslist list of list, each sublist being a matching pair of gold and guess BratDataModel results
    :param comparator, function that can compare two brat_dm instances and update a classification result
    :returns map from mention types to classification results
    """
    typeset=set()
    for it in reslist:
        typeset.update(it[0].mentiontypes())
        typeset.update(it[1].mentiontypes())

    retmap = {}
    for ls in typeset:
        res=SRClassification()
        for i in range(0, len(reslist)):
            srcomparator.compare(reslist[i][0], reslist[i][1], res, ls)
        retmap[ls]=res
    return retmap


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
        print("getdirs add gold "+str(gold_bdms[key])+", guess "+str(guess_bdms[key]))

    if (len(to_skip))>0:
        print("Warning: number of skipped files "+len(to_skip))
        for item in to_skip:
              print(" skipped file "+str(item))



    return res


def evaluate_directories(golddir, guessdir, srcomparator):
    """ Primary method for running evaluations.
    :param gold_dir: director holding gold results
    :param guess_dir: director holding guess results
    :param srcomparator: a comparator to use
    :return map from annotation types to results for those labels, ALL for overall results
    """
    bdmslist = compare_dirs(golddir, guessdir)
    resmap = compare_mention_list_by_type(bdmslist, srcomparator)
    resmap["ALL"]=compare_mention_list(bdmslist, srcomparator)
    return resmap


def main():
    parser = argparse.ArgumentParser(description='Evaluate TAC 2018 Systematic Review Methods')
    parser.add_argument('--gold_dir', metavar='GOLD', required=True, type=str, help='path to directory containing human curated data')
    parser.add_argument('--guess_dir', metavar='GUESS', required=True, type=str, help='path to directory containing model generated data')
    parser.add_argument('--res_file', metavar='RESFILE', required=True, type=str, help='filenane to write results to')
    parser.add_argument('--threshold', metavar='THRESHOLD', required=True, type=float, help='threshold for classification (0-1)')
    args = parser.parse_args()

    with open(args.res_file, 'w') as out_file:
        out_file.write('Results\n')
        out_file.write("Gold directory "+args.gold_dir+"\n")
        out_file.write("Guess directory " + args.guess_dir + "\n")
        out_file.write("Threshold " + str(args.threshold) + "\n")
        resmap = evaluate_directories(args.gold_dir, args.guess_dir, SRComparator(args.threshold))
        mtypes=sorted(list(resmap.keys()))
        for mtype in mtypes:
            out_file.write("Results for type " + str(mtype) + " is\t\t" + str(resmap[mtype])+"\n")


if __name__ == "__main__":
    main()






