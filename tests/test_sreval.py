import sreval.evaluation
import sreval.brat_dm
from sreval.evaluation import SRComparator, evaluate_directories
from sreval.brat_dm import BratDataModel, MentionAnnotation, GroupAnnotation, GroupModel
import pytest
import os


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
        srcomp=SRComparator(0.51)
        evaluate_directories("./testfiles/dircompare/gold_mismatch",
                             "./testfiles/dircompare/estimated_mismatch",srcomp)




def test_dir_good():
    """ test of estimated versus gold directories, should succeed and give outputs """

    srcomp=SRComparator(0.51)
    resmap = evaluate_directories("./testfiles/dircompare/gold",
                                  "./testfiles/dircompare/estimated",srcomp)
    assert len(resmap)==2
    assert resmap['Dose'].tp==4
    assert resmap['Dose'].fp==0
    assert resmap['Dose'].fn==0

    assert resmap['ALL'].tp==4
    assert resmap['ALL'].fp==0
    assert resmap['ALL'].fn==0


def test_basicmatch():

    srcomp=SRComparator(0.51)
    resmap = evaluate_directories("./testfiles/basicmatch/gold",
                                  "./testfiles/basicmatch/estimated",srcomp)

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

    srcomp=SRComparator(0.51)
    resmap = evaluate_directories("./testfiles/overlapmatch1/gold",
                                  "./testfiles/overlapmatch1/estimated",srcomp)
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
    srcomp = SRComparator(0.75)
    resmap = evaluate_directories("./testfiles/overlapmatch1/gold",
                                  "./testfiles/overlapmatch1/estimated", srcomp)
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
    srcomp = SRComparator(0.50)
    resmap = evaluate_directories("./testfiles/multi_alloc/gold",
                                  "./testfiles/multi_alloc/estimated", srcomp)
    assert len(resmap) == 2
    assert resmap['Mention1'].tp == 2
    assert resmap['Mention1'].fp == 3
    assert resmap['Mention1'].fn == 3
    assert resmap['ALL'].tp == 2
    assert resmap['ALL'].fp == 3
    assert resmap['ALL'].fn == 3

def test_multi_alloc2():
    srcomp = SRComparator(0.10)
    resmap = evaluate_directories("./testfiles/multi_alloc/gold",
                                  "./testfiles/multi_alloc/estimated", srcomp)
    assert len(resmap) == 2
    assert resmap['Mention1'].tp == 4
    assert resmap['Mention1'].fp == 1
    assert resmap['Mention1'].fn == 1
    assert resmap['ALL'].tp == 4
    assert resmap['ALL'].fp == 1
    assert resmap['ALL'].fn == 1

def test_multi_alloc3():
    srcomp = SRComparator(0.01)
    resmap = evaluate_directories("./testfiles/multi_alloc/gold",
                                  "./testfiles/multi_alloc/estimated", srcomp)
    assert len(resmap) == 2
    assert resmap['Mention1'].tp == 5
    assert resmap['Mention1'].fp == 0
    assert resmap['Mention1'].fn == 0
    assert resmap['ALL'].tp == 5
    assert resmap['ALL'].fp == 0
    assert resmap['ALL'].fn == 0


def test_multi_overlap1():
    srcomp = SRComparator(0.7)
    resmap = evaluate_directories("./testfiles/overlap_multiloc/gold",
                                  "./testfiles/overlap_multiloc/estimated", srcomp)
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
    srcomp = SRComparator(0.55)
    resmap = evaluate_directories("./testfiles/overlap_multiloc/gold",
                                  "./testfiles/overlap_multiloc/estimated", srcomp)
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
    srcomp = SRComparator(0.45)
    resmap = evaluate_directories("./testfiles/overlap_multiloc/gold",
                                  "./testfiles/overlap_multiloc/estimated", srcomp)
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



