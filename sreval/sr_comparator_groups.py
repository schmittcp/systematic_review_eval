"""

This class holds methods used to compare a set of annotation group models

Comparison of two groups is based on the mentions associated with the group, e.g,
  G1 holds mentions m11, m12, and m13
  G2 holds mentions m21, m24, m25, and m26

  the overlap is computed as 1/(7) assuming that m11 matches m21.

  This means we have to have a way to know that mention m11 matches mention m21.  So
  this algorithm depends on the mention matching algorithms having created a matching
  of mentions.

  



"""
import argparse
import os
from brat_dm import BratDataModel
import numpy as np
from scipy.optimize import linear_sum_assignment
import traceback
from srresult import SRResult
import random

def compare_groups(reslist, threshold):
    """ compare gold results versus model results
    :param reslist list of list, each sublist holds a triple representing a paired set of guess and gold brat data models
           reslist[i][0] = the gold brat data model
           reslist[i][1] = the guess brat data model that matches the guess brat data model
           reslist[i][2] = matched mentions between the guess and gold data models.  This is a dictionary where the
                           key is a mention annotation from the guess data model and the value is the matched mention
                           annotation from the gold data model.  Unmatched annotations are not in the dictionary.
                           Dictionary only holds the mention ids.

    :returns map from group types to classification results, including ALL for all group types
    """
    comparator = SRComparator_Groups(threshold)

    typeset = set()
    for it in reslist:
        typeset.update(it[0].groupmodeltypes())
        typeset.update(it[1].groupmodeltypes())
    retmap = {}

    for ls in typeset:
        retmap[ls] = SRResult()
        for i in range(0, len(reslist)):
            comparator.compare(reslist[i][0], reslist[i][1], reslist[i][2], retmap[ls], ls)

    retmap["ALL"] = SRResult()
    for i in range(0, len(reslist)):
        comparator.compare(reslist[i][0], reslist[i][1], reslist[i][2], retmap["ALL"])

    return retmap


class SRComparator_Groups:
    """ Compares sets of group models (brat_dm mentions) """

    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def compare(self, golddm, guessdm, matched_mentions, res, mtype=None):
        """ compare gold mention results versus guess mention results on a single data set
        :param golddm gold BratDataModel instance
        :param guessdm guess BratDataModel instance
        :param matched_mentions dictionary holding the assignment of BratDataModel MentionAnnotations from the 
                  guess brat data models to the MentionAnnotations from the gold brat data models.  Dictionary
                  only holds MentionAnnotations for which a mapping exists.Dictionary only holds the mention ids.
        :param res, classification instance holding results, to be updated by this method
        :param mtype, mention type to restrict results to, if none will process all types

        """
        if mtype is None:
            gold_list = [m for m in golddm.allgroupmodels()]
            guess_list = [m for m in guessdm.allgroupmodels()]
        else:
            gold_list = [m for m in golddm.groupmodels_by_types(mtype)]
            guess_list = [m for m in guessdm.groupmodels_by_types(mtype)]

        guess_ind = get_assignments(guess_list, gold_list, matched_mentions, self.threshold)

        """ now calculate the scores.  If a guess was assigned to a gold with a overlap score
            of 1.0, then there is no actual match for the guess (e.g., a false positive).  If 
            a guess has no match or if the match is below the overlap threshold, then score it
            as a false positive.  If a gold has no match above overlap threshold, then score 
            it as a false negative 
        """
        goldhit = [0] * len(gold_list)
        for guessi in range(0, len(guess_list)):
            if guess_ind[guessi] >= 0:
                res.tp += 1
                goldhit[guess_ind[guessi]] = 1
            else:
                res.fp += 1

        for goldi in range(0, len(gold_list)):
            if goldhit[goldi] == 0:
                res.fn += 1

def get_assignments(guess_list, gold_list, matched_mentions, threshold):
    """ 
           Create assignment between group models in the guess list and group models in the gold list
           :param guess_list list of BratDataModel GroupModel instances
           :param gold_list list of BratDataModel GroupModel instances
           :param matched_mentions dictionary holding the assignment of BratDataModel MentionAnnotations from the 
                  guess brat data models to the MentionAnnotations from the gold brat data models.  Dictionary
                  only holds MentionAnnotations for which a mapping exists.  Dictionary only holds the mention ids.
           :threshold the threshold below which matches are ignored (0.01-0.99)

           This algorithm computes the overlap between each pair of group models then assigns
           unique pairings using the scipy.optimize.linear_sum_assignment module.
           :return list of size guess_list with assignment for each, if -1 then no assignment
    """

    # get cost matrix, should be square, set to large value (high cost) as default
    cost_max=1.0-threshold
    mhigh = 10.0
    mlen = max(len(guess_list), len(gold_list))
    mcost = mhigh * np.ones((mlen, mlen))
    for guessi in range(0, len(guess_list)):
        for goldi in range(0, len(gold_list)):
            overlap = get_overlap(guess_list[guessi], gold_list[goldi], matched_mentions)
            sizeguess = len(guess_list[guessi].mentions)
            sizegold = len(gold_list[goldi].mentions)
            mcost[guessi, goldi] = 1.0 - (2.0 * overlap / (sizegold + sizeguess))
            if mcost[guessi, goldi] > cost_max:
                mcost[guessi, goldi] = mhigh

    row_ind, col_ind = linear_sum_assignment(mcost)

    retl = len(guess_list) * [-1]
    for i in range(0, len(retl)):
        if mcost[i, col_ind[i]] < mhigh:
            retl[i] = col_ind[i]
    return retl

def get_overlap(guessgm, goldgm, matched_mentions):
    """ get the overlap between two group models, zero if none or different types 
            matched_mentions is a dictionary matching mentions from the parent brat data models
    """
    if guessgm.grouptype != goldgm.grouptype:
        return 0
    overlap=0
    goldmaids=set([x.maid for x in goldgm.mentions])
    for guessma in guessgm.mentions:
        guessmaid = guessma.maid
        if guessmaid in matched_mentions:
            goldmaid = matched_mentions[guessmaid]
            if goldmaid in goldmaids:
                overlap = overlap+1
    return overlap
