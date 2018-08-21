import sreval.evaluation
import sreval.brat_dm
from evaluation import compare_dirs
from sr_comparator_mentions import compare_mentions, get_mention_mappings
from sr_comparator_groups import compare_groups
from sreval.brat_dm import BratDataModel, MentionAnnotation, GroupAnnotation, GroupModel
import pytest
import os


def test_grpbasic4_1():
    bdmslist = compare_dirs("./testfiles/grpbasic4/test1/gold","./testfiles/grpbasic4/test1/estimated")

    # gold:  groups g1, g2, g3
    # est:   groups e1, e2
    # ov:    e1-g1: 0.66,  e1-g2: 0.85, e1-g3: 0.66
    # ov:    e2-g1: 0.00,  e2-g2: 0.66, e2-g3: 0.40

    # e1-g1, e2-g2 is right, so both links are at 0.66
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.6)
    assert len(resmap)==2
    assert resmap['Equiv'].tp==2
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==2
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==1

    # e1-g1, e2-g2
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.3)
    assert len(resmap)==2
    assert resmap['Equiv'].tp==2
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==2
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==1

    # e1-g2, e2-nil
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.68)
    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==2

    # e1-nill, e2-nil
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.88)
    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==2
    assert resmap['Equiv'].fn==3
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==2
    assert resmap['ALL'].fn==3



def test_grpbasic4_0():
    bdmslist = compare_dirs("./testfiles/grpbasic4/test0/gold","./testfiles/grpbasic4/test0/estimated")

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.3)
    assert len(resmap)==2
    assert resmap['Equiv'].tp==2
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==2
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.4)
    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1



def test_grpbasic3_0():
    bdmslist = compare_dirs("./testfiles/grpbasic3/test0/gold","./testfiles/grpbasic3/test0/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.51)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==0

def test_grpbasic3_1():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test1/gold","./testfiles/grpbasic2/test1/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.51)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.19)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic3_2():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test2/gold","./testfiles/grpbasic2/test2/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.67)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.65)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic3_3():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test3/gold","./testfiles/grpbasic2/test3/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.86)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.84)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic3_4():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test4/gold","./testfiles/grpbasic2/test4/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.99)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic3_5():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test5/gold","./testfiles/grpbasic2/test5/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.89)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.87)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic2_0():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test0/gold","./testfiles/grpbasic2/test0/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.51)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==1

def test_grpbasic2_1():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test1/gold","./testfiles/grpbasic2/test1/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.51)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.19)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic2_2():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test2/gold","./testfiles/grpbasic2/test2/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.67)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.65)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic2_3():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test3/gold","./testfiles/grpbasic2/test3/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.86)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.84)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic2_4():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test4/gold","./testfiles/grpbasic2/test4/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.99)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic2_5():
    bdmslist = compare_dirs("./testfiles/grpbasic2/test5/gold","./testfiles/grpbasic2/test5/estimated")
    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.89)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==1
    assert resmap['Equiv'].fn==1
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==1
    assert resmap['ALL'].fn==1

    comlist = get_mention_mappings(bdmslist, 0.51)
    resmap = compare_groups(comlist, 0.87)

    assert len(resmap)==2
    assert resmap['Equiv'].tp==1
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==0
    assert resmap['ALL'].tp==1
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_grpbasic_mention_match():
    bdmslist = compare_dirs("./testfiles/grpbasic/testmatch/gold","./testfiles/grpbasic/testmatch/estimated")
    comlist = get_mention_mappings(bdmslist, 0.9)
    
    assert len(comlist)==1
    assert len(comlist[0])==3

    assert len(comlist[0][2])==9
    assert "T11" not in comlist[0][2]
    assert "T12" not in comlist[0][2]
    assert "T13" not in comlist[0][2]
    assert comlist[0][2]["T35"] == "T351"
    assert comlist[0][2]["T36"] == "T361"
    assert comlist[0][2]["T37"] == "T371"
    assert comlist[0][2]["T38"] == "T381"
    assert comlist[0][2]["T39"] == "T391"
    assert "T140" not in comlist[0][2]
    assert comlist[0][2]["T50"] == "T501"
    assert "T151" not in comlist[0][2]
    assert comlist[0][2]["T54"] == "T541"
    assert comlist[0][2]["T56"] == "T561"
    assert "T157" not in comlist[0][2]
    assert comlist[0][2]["T58"] == "T581"

def test_grpbasic0():
    bdmslist = compare_dirs("./testfiles/grpbasic/test0/gold","./testfiles/grpbasic/test0/estimated")
    comlist = get_mention_mappings(bdmslist, 0.5)
    resmap = compare_groups(comlist, 0.51)

    assert len(resmap)==4
    assert resmap['TestArticleGroup'].tp==0
    assert resmap['TestArticleGroup'].fp==1
    assert resmap['TestArticleGroup'].fn==3
    assert resmap['Animal'].tp==0
    assert resmap['Animal'].fp==1
    assert resmap['Animal'].fn==1
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==2
    assert resmap['ALL'].fn==6


def test_grpbasic11():
    bdmslist = compare_dirs("./testfiles/grpbasic/test1/gold","./testfiles/grpbasic/test1/estimated")
    comlist = get_mention_mappings(bdmslist, 0.5)
    resmap = compare_groups(comlist, 0.51)

    assert len(resmap)==4
    assert resmap['TestArticleGroup'].tp==0
    assert resmap['TestArticleGroup'].fp==1
    assert resmap['TestArticleGroup'].fn==3
    assert resmap['Animal'].tp==0
    assert resmap['Animal'].fp==1
    assert resmap['Animal'].fn==1
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==2
    assert resmap['ALL'].fn==6


def test_grpbasic12():
    bdmslist = compare_dirs("./testfiles/grpbasic/test1/gold","./testfiles/grpbasic/test1/estimated")
    comlist = get_mention_mappings(bdmslist, 0.5)
    resmap = compare_groups(comlist, 0.25)

    assert len(resmap)==4
    assert resmap['TestArticleGroup'].tp==1
    assert resmap['TestArticleGroup'].fp==0
    assert resmap['TestArticleGroup'].fn==2
    assert resmap['Animal'].tp==1
    assert resmap['Animal'].fp==0
    assert resmap['Animal'].fn==0
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==2
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==4


def test_grpbasic21():
    bdmslist = compare_dirs("./testfiles/grpbasic/test2/gold","./testfiles/grpbasic/test2/estimated")
    comlist = get_mention_mappings(bdmslist, 0.5)
    resmap = compare_groups(comlist, 0.31)

    assert len(resmap)==4
    assert resmap['TestArticleGroup'].tp==1
    assert resmap['TestArticleGroup'].fp==0
    assert resmap['TestArticleGroup'].fn==2
    assert resmap['Animal'].tp==1
    assert resmap['Animal'].fp==0
    assert resmap['Animal'].fn==0
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==2
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==4


def test_grpbasic22():
    bdmslist = compare_dirs("./testfiles/grpbasic/test2/gold","./testfiles/grpbasic/test2/estimated")
    comlist = get_mention_mappings(bdmslist, 0.5)
    resmap = compare_groups(comlist, 0.75)   # animal goes away but testarticle still matches

    assert resmap['TestArticleGroup'].tp==0
    assert resmap['TestArticleGroup'].fp==1
    assert resmap['TestArticleGroup'].fn==3
    assert resmap['Animal'].tp==0
    assert resmap['Animal'].fp==1
    assert resmap['Animal'].fn==1
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==0
    assert resmap['ALL'].fp==2
    assert resmap['ALL'].fn==6


def test_grpbasic3():
    bdmslist = compare_dirs("./testfiles/grpbasic/test3/gold","./testfiles/grpbasic/test3/estimated")
    comlist = get_mention_mappings(bdmslist, 0.5)
    resmap = compare_groups(comlist, 0.75)

    assert resmap['TestArticleGroup'].tp==1
    assert resmap['TestArticleGroup'].fp==0
    assert resmap['TestArticleGroup'].fn==2
    assert resmap['Animal'].tp==1
    assert resmap['Animal'].fp==0
    assert resmap['Animal'].fn==0
    assert resmap['Equiv'].tp==0
    assert resmap['Equiv'].fp==0
    assert resmap['Equiv'].fn==2
    assert resmap['ALL'].tp==2
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==4



def test_parse_xml_files():
    """ test parsing the xml files """
    bmd = BratDataModel("test","./testfiles/parsexml/PMC2607137.xml")
    ms = bmd.allmentions()
    gs = bmd.allgroups()
    gm = bmd.allgroupmodels()
    assert len(ms) == 74
    assert len(gs) == 11
    assert len(gm) == 5

    bmd = BratDataModel("test","./testfiles/parsexml/PMC2680977.xml")
    ms = bmd.allmentions()
    gs = bmd.allgroups()
    gm = bmd.allgroupmodels()
    assert len(ms) == 62
    assert len(gs) == 18
    assert len(gm) == 7

    try:
        bmd = BratDataModel("./testfiles/parsexml/badxml.xml")
        assert False
    except:
        assert True

                                
def test_dir_missing_files():
    """ test of estimated_mismatch and gold_mismatch, should fail on missing estiamted annotation files """
    with pytest.raises(ValueError):
        bdmslist = compare_dirs("./testfiles/dircompare/gold_mismatch", "./testfiles/dircompare/estimated_mismatch")
        resmap = compare_mentions(bdmslist, 0.51)




def test_dir_good():
    """ test of estimated versus gold directories, should succeed and give outputs """

    bdmslist = compare_dirs("./testfiles/dircompare/gold","./testfiles/dircompare/estimated")
    resmap = compare_mentions(bdmslist, 0.51)

    assert len(resmap)==2
    assert resmap['Dose'].tp==4
    assert resmap['Dose'].fp==0
    assert resmap['Dose'].fn==0

    assert resmap['ALL'].tp==4
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_basicmatch():

    bdmslist = compare_dirs("./testfiles/basicmatch/gold","./testfiles/basicmatch/estimated")
    resmap = compare_mentions(bdmslist, 0.51)

    assert len(resmap)==4
    assert resmap['Dose'].tp==0
    assert resmap['Dose'].fp==1
    assert resmap['Dose'].fn==2

    assert resmap['GroupName'].tp==2
    assert resmap['GroupName'].fp==1
    assert resmap['GroupName'].fn==2

    assert resmap['Endpoint'].tp==8
    assert resmap['Endpoint'].fp==0
    assert resmap['Endpoint'].fn==0

    assert resmap['ALL'].tp==10
    assert resmap['ALL'].fp==2
    assert resmap['ALL'].fn==4


def test_overlap1():
    bdmslist = compare_dirs("./testfiles/overlapmatch1/gold","./testfiles/overlapmatch1/estimated")
    resmap = compare_mentions(bdmslist, 0.51)

    assert len(resmap)==10
    assert resmap['Species'].tp==0
    assert resmap['Species'].fp==1
    assert resmap['Species'].fn==1
    assert resmap['Sex'].tp==0
    assert resmap['Sex'].fp==1
    assert resmap['Sex'].fn==1
    assert resmap['Endpoint'].tp==1
    assert resmap['Endpoint'].fp==0
    assert resmap['Endpoint'].fn==0
    assert resmap['Groupname'].tp==0
    assert resmap['Groupname'].fp==1
    assert resmap['Groupname'].fn==1
    assert resmap['TimeUnits'].tp==0
    assert resmap['TimeUnits'].fp==1
    assert resmap['TimeUnits'].fn==1
    assert resmap['EndpointMethod'].tp==1
    assert resmap['EndpointMethod'].fp==0
    assert resmap['EndpointMethod'].fn==0
    assert resmap['groupsize'].tp==1
    assert resmap['groupsize'].fp==0
    assert resmap['groupsize'].fn==0
    assert resmap['NewGuessLabel'].tp==0
    assert resmap['NewGuessLabel'].fp==1
    assert resmap['NewGuessLabel'].fn==0
    assert resmap['NewGoldLabel'].tp==0
    assert resmap['NewGoldLabel'].fp==0
    assert resmap['NewGoldLabel'].fn==1
    assert resmap['ALL'].tp==3
    assert resmap['ALL'].fp==5
    assert resmap['ALL'].fn==5




def test_overlap2():
    bdmslist = compare_dirs("./testfiles/overlapmatch1/gold","./testfiles/overlapmatch1/estimated")
    resmap = compare_mentions(bdmslist, 0.75)

    assert len(resmap) == 10
    assert resmap['Species'].tp == 0
    assert resmap['Species'].fp == 1
    assert resmap['Species'].fn == 1
    assert resmap['Sex'].tp == 0
    assert resmap['Sex'].fp == 1
    assert resmap['Sex'].fn == 1
    assert resmap['Endpoint'].tp == 1
    assert resmap['Endpoint'].fp == 0
    assert resmap['Endpoint'].fn == 0
    assert resmap['Groupname'].tp == 0
    assert resmap['Groupname'].fp == 1
    assert resmap['Groupname'].fn == 1
    assert resmap['TimeUnits'].tp == 0
    assert resmap['TimeUnits'].fp == 1
    assert resmap['TimeUnits'].fn == 1
    assert resmap['EndpointMethod'].tp == 0
    assert resmap['EndpointMethod'].fp == 1
    assert resmap['EndpointMethod'].fn == 1
    assert resmap['groupsize'].tp == 0
    assert resmap['groupsize'].fp == 1
    assert resmap['groupsize'].fn == 1
    assert resmap['NewGuessLabel'].tp == 0
    assert resmap['NewGuessLabel'].fp == 1
    assert resmap['NewGuessLabel'].fn == 0
    assert resmap['NewGoldLabel'].tp == 0
    assert resmap['NewGoldLabel'].fp == 0
    assert resmap['NewGoldLabel'].fn == 1
    assert resmap['ALL'].tp == 1
    assert resmap['ALL'].fp == 7
    assert resmap['ALL'].fn == 7


def test_multi_alloc1():
    bdmslist = compare_dirs("./testfiles/multi_alloc/gold","./testfiles/multi_alloc/estimated")
    resmap = compare_mentions(bdmslist, 0.50)

    assert len(resmap) == 2
    assert resmap['Mention1'].tp == 2
    assert resmap['Mention1'].fp == 3
    assert resmap['Mention1'].fn == 3
    assert resmap['ALL'].tp == 2
    assert resmap['ALL'].fp == 3
    assert resmap['ALL'].fn == 3

def test_multi_alloc2():
    bdmslist = compare_dirs("./testfiles/multi_alloc/gold","./testfiles/multi_alloc/estimated")
    resmap = compare_mentions(bdmslist, 0.10)

    assert len(resmap) == 2
    assert resmap['Mention1'].tp == 4
    assert resmap['Mention1'].fp == 1
    assert resmap['Mention1'].fn == 1
    assert resmap['ALL'].tp == 4
    assert resmap['ALL'].fp == 1
    assert resmap['ALL'].fn == 1

def test_multi_alloc3():
    bdmslist = compare_dirs("./testfiles/multi_alloc/gold","./testfiles/multi_alloc/estimated")
    resmap = compare_mentions(bdmslist, 0.01)

    assert len(resmap) == 2
    assert resmap['Mention1'].tp == 5
    assert resmap['Mention1'].fp == 0
    assert resmap['Mention1'].fn == 0
    assert resmap['ALL'].tp == 5
    assert resmap['ALL'].fp == 0
    assert resmap['ALL'].fn == 0


def test_multi_overlap1():
    bdmslist = compare_dirs("./testfiles/overlap_multiloc/gold","./testfiles/overlap_multiloc/estimated")
    resmap = compare_mentions(bdmslist, 0.7)

    assert len(resmap) == 6
    assert resmap['Mention1'].tp == 0
    assert resmap['Mention1'].fp == 1
    assert resmap['Mention1'].fn == 1
    assert resmap['Mention2'].tp == 1
    assert resmap['Mention2'].fp == 0
    assert resmap['Mention2'].fn == 0
    assert resmap['Mention3'].tp == 0
    assert resmap['Mention3'].fp == 1
    assert resmap['Mention3'].fn == 1
    assert resmap['Mention4'].tp == 0
    assert resmap['Mention4'].fp == 1
    assert resmap['Mention4'].fn == 1
    assert resmap['Mention5'].tp == 0
    assert resmap['Mention5'].fp == 1
    assert resmap['Mention5'].fn == 1
    assert resmap['ALL'].tp == 1
    assert resmap['ALL'].fp == 4
    assert resmap['ALL'].fn == 4



def test_multi_overlap2():
    bdmslist = compare_dirs("./testfiles/overlap_multiloc/gold","./testfiles/overlap_multiloc/estimated")
    resmap = compare_mentions(bdmslist, 0.55)

    assert len(resmap) == 6
    assert resmap['Mention1'].tp == 0
    assert resmap['Mention1'].fp == 1
    assert resmap['Mention1'].fn == 1
    assert resmap['Mention2'].tp == 1
    assert resmap['Mention2'].fp == 0
    assert resmap['Mention2'].fn == 0
    assert resmap['Mention3'].tp == 0
    assert resmap['Mention3'].fp == 1
    assert resmap['Mention3'].fn == 1
    assert resmap['Mention4'].tp == 0
    assert resmap['Mention4'].fp == 1
    assert resmap['Mention4'].fn == 1
    assert resmap['Mention5'].tp == 1
    assert resmap['Mention5'].fp == 0
    assert resmap['Mention5'].fn == 0
    assert resmap['ALL'].tp == 2
    assert resmap['ALL'].fp == 3
    assert resmap['ALL'].fn == 3


def test_multi_overlap3():
    bdmslist = compare_dirs("./testfiles/overlap_multiloc/gold","./testfiles/overlap_multiloc/estimated")
    resmap = compare_mentions(bdmslist, 0.45)

    assert len(resmap) == 6
    assert resmap['Mention1'].tp == 0
    assert resmap['Mention1'].fp == 1
    assert resmap['Mention1'].fn == 1
    assert resmap['Mention2'].tp == 1
    assert resmap['Mention2'].fp == 0
    assert resmap['Mention2'].fn == 0
    assert resmap['Mention3'].tp == 1
    assert resmap['Mention3'].fp == 0
    assert resmap['Mention3'].fn == 0
    assert resmap['Mention4'].tp == 1
    assert resmap['Mention4'].fp == 0
    assert resmap['Mention4'].fn == 0
    assert resmap['Mention5'].tp == 1
    assert resmap['Mention5'].fp == 0
    assert resmap['Mention5'].fn == 0
    assert resmap['ALL'].tp == 4
    assert resmap['ALL'].fp == 1
    assert resmap['ALL'].fn == 1



