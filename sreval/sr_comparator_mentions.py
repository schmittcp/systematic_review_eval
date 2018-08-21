"""

This class holds methods used to compare a set of annotation mentions


"""
import argparse
import os
from brat_dm import BratDataModel
import numpy as np
from scipy.optimize import linear_sum_assignment
import traceback
from srresult import SRResult
 


def get_mention_mappings(reslist, threshold):
    """ match guess mentions to gold mentions
    :param reslist list of list, each sublist being a matching pair of gold and guess BratDataModel results
    :return retlist list of list, each sublist holds a triple representing a paired set of guess and gold brat data models
           retlist[i][0] = the gold brat data model
           retlist[i][1] = the guess brat data model that matches the guess brat data model
           retlist[i][2] = matched mentions between the guess and gold data models.  This is a dictionary where the
                           key is a mention annotation from the guess data model and the value is the matched mention
                           annotation from the gold data model.  Unmatched annotations are not in the dictionary.
                           Dictionary only holds the mention ids.
    """
    retlist=[]
    comparator=SRComparator_Mentions(threshold)
    for i in range(0, len(reslist)):
        map=comparator.get_mention_mappings(reslist[i][0], reslist[i][1])
        res=[reslist[i][0],reslist[i][1],map]
        retlist.append(res)
    return retlist


def compare_mentions(reslist, threshold):
    """ compare gold results versus model results
    :param reslist list of list, each sublist being a matching pair of gold and guess BratDataModel results
    :returns map from mention types to classification results, including ALL for all mention types
    """
    comparator=SRComparator_Mentions(threshold)

    typeset=set()
    for it in reslist:
        typeset.update(it[0].mentiontypes())
        typeset.update(it[1].mentiontypes())

    retmap = {}
    for ls in typeset:
        retmap[ls]=SRResult()
        for i in range(0, len(reslist)):
            comparator.compare(reslist[i][0], reslist[i][1], retmap[ls], ls)

    retmap["ALL"]=SRResult()
    for i in range(0, len(reslist)):
        comparator.compare(reslist[i][0], reslist[i][1], retmap["ALL"])

    return retmap


class SRComparator_Mentions:
    """ Compares sets of mentions (brat_dm mentions) """

    def __init__(self, threshold=0.5):
        self.threshold = threshold


    def get_mention_mappings(self, golddm, guessdm):
        """ similar to compare, this method returns the mapping of guess mentions to gold mentions on a single data set for all mention types 
        :param golddm gold BratDataModel instance
        :param guessdm guess BratDataModel instance
        :return dictionary from guess mention id to matching gold mention id, if not assigned guess mention id will not be in the dictionary
        """
        gold_list = [m for m in golddm.allmentions()]
        guess_list = [m for m in guessdm.allmentions()]
        guess_ind=get_assignments(guess_list,gold_list,self.threshold)
        retmap={}
        for guessi in range(0, len(guess_list)):
            if guess_ind[guessi]>=0:
                guessid=guess_list[guessi].maid
                goldid=gold_list[guess_ind[guessi]].maid
                retmap[guessid] = goldid
        return retmap



    def compare(self, golddm, guessdm, res, mtype=None):
        """ compare gold mention results versus guess mention results on a single data set 
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

        guess_ind=get_assignments(guess_list,gold_list,self.threshold)

        """ now calculate the scores.  If a guess was assigned to a gold with a overlap score
            of 1.0, then there is no actual match for the guess (e.g., a false positive).  If 
            a guess has no match or if the match is below the overlap threshold, then score it
            as a false positive.  If a gold has no match above overlap threshold, then score 
            it as a false negative 
        """
        guesshits=set()
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



def get_assignments(guess_list, gold_list, threshold):
    """ assign each mention annotation from guess_list to a mention annotation from gold_list
        such that guess are assigned preferentially to elements of gold
        that they have greater overlap with.
        :param guess_list list of BratDataModel MentionAnnotion instances
        :param gold_list list of BratDataModel MentionAnnotation instances
        :threshold the threshold below which matches are ignored (0.01-0.99)
        :return list of size guess_list with assignment for each, if -1 then no assignment

        Fundamentally, this is a bipartite graph matching problem and there are varying ways of
        solving it.  We use the hungarian algorithm as it allows weighted matrix and the scipy
        implementation: scipy.optimize.linear_sum_assignment
    """

    # get cost matrix, should be square, set to large value (high cost) as default
    cost_max=1.0-threshold
    mhigh=10.0
    mlen=max(len(guess_list),len(gold_list))
    mcost = mhigh*np.ones((mlen,mlen))
    for guessi in range(0, len(guess_list)):
        for goldi in range(0, len(gold_list)):
                overlap = get_overlap(guess_list[guessi], gold_list[goldi])
                lengold = getsumdiffs(gold_list[goldi].malocs)
                lenguess = getsumdiffs(guess_list[guessi].malocs)
                mcost[guessi, goldi] = 1.0-(2.0*overlap/(lengold+lenguess))
                if mcost[guessi, goldi]>cost_max:
                    mcost[guessi, goldi]=mhigh

    row_ind, col_ind = linear_sum_assignment(mcost)

    retl=len(guess_list)*[-1]
    for i in range(0,len(retl)):
        if mcost[i,col_ind[i]]<mhigh:
            retl[i]=col_ind[i]

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
    """ given two lists l1[i,j] and l2[k,l] return the overlap,
        e.g., l1[2,5] and l2[4,6] has an overlap of 1 """
    if seg1[1] < seg2[0] or seg1[0] > seg2[1]:
        return 0
    return min(seg1[1], seg2[1])-max(seg1[0], seg2[0])
