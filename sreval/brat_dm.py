"""

This module holds annotations read in from file.  Input file format
is the NIST TAC 2018 XML format for the Systematic Review challenge
which is based off the Brat annotation format.

Annotations include mentions and groupings of mentions.

This file contains four classes:

MentionAnnotation: class that represents a single mention annotation
GroupAnnotation: class that represents a single group-to-mention annotation
GroupModel: class that represents a single group and all its associated mentions
BratDataModel: class that represents a single annotated document, holds all the
    mentionannotations, groupannotations, and groupmodels.

"""
import re
import xml.etree.ElementTree as ET





class MentionAnnotation:
    """  class to represent a single mention annotation, that includes the
         annotation, the location of the annotations in the document and the
         text.  Note that the location can include multiple locations in order
         to handle discontinuous text

         examples:
         T36	Endpoint 1741 1756	vaginal opening  4
         T37	Endpoint 2135 2148;2153 2159	organ weights uterus  6

        maid            holds mention annotation id (e.g., T36)
        matype          holds mention type (e.g., Endpoint)
        malocs          holds locations {[start1,end1],...[startn,endn]}
        matext          holds mention text

    """

    def __init__(self, maid, matype, malocs, matext):
        """ define a new mention annotation
        :param: annstr string holding mention annotation in xml notation
        """
        self.maid = maid
        self.matype = matype
        self.malocs = self.__splitlocs__(malocs)
        self.matext = matext

    def __splitlocs__(self, smalocs):
        """ split locs in string into a set of list pairs {[],[]}"""
        """7311 7318;7332 7337;7360 7365 """
        xs = [x.split(' ') for x in smalocs.split(';')]
        x = [[int(float(j)) for j in i] for i in xs]
        return x

    def __str__(self):
        sl=' '.join([str(self.malocs[0][0]),str(self.malocs[0][1])])
        for i in range(1,len(self.malocs)):
            tsl=' '.join([str(self.malocs[i][0]),str(self.malocs[i][1])])
            sl=';'.join([sl,tsl])


        return self.maid+"\t"+self.matype+' '+sl+'\t'+self.matext


class GroupAnnotation:
    """  class to represent a single group annotation, this includes the 
         group type, the group number, and the mention being added to the group

         examples:
         A21    GROUP__TestArticleGroup-4 T104
         A15    GROUP_Animal-0 T1

        gaid             holds group id (e.g., A21)
        galabel          holds group type TestArticleGroup
        gatypeid         holds group type id 4
        gamention        holds mention id (e.g., T104)
    """
    def __init__(self, ingaid, ingatype, ingatypeid, ingamention):
        self.gaid = ingaid
        self.gatype = ingatype
        self.gatypeid = ingatypeid
        self.gamention = ingamention

    def __str__(self):
        return str(self.gaid)+'\t'+str(self.galabel)+'\t'+str(self.gatypeid)+'\t'+str(self.gamention)


class GroupModel:
    """ class to represent a grouping of mention annotations created from group annotations
    
        groupid     TestArticleGroup-4
        grouptype   TestArticleGroup
        mentions    list of MentionAnnotations
    """
    def __init__(self, groupid, grouptype):
        """ create gorup model with given id, id is of form GROUP_groupname """
        self.groupid = groupid
        self.grouptype = grouptype
        self.mentions = []
        self.isok = False

    def __gettype__(self,gid):
        """ parse group type from group id """
        gid = re.sub(r'GROUP[_]+', '', gid)
        gid = re.sub(r'[-(0-9)+]', '', gid)
        return gid

    def __str__(self):
        s = self.groupid+", "+self.grouptype
        for m in self.mentions:
            s = '\n\t'.join([s,str(m)])
        return s

class BratDataModel:
    """
    Model for annotations from a document

    name = name of document
    annotations = list of mention and group annotations
    groupmodels = list of groupmodels
    """

    def __init__(self, name=None, annotationfilename=None):
        """
        Construct an brat data model
       :param annotationfilename: name of brat annotation file in xml format, if None then build empty mode (see read_annotations)
        """
        self.name = name
        self.annotations = []
        self.groupmodels = []
        if annotationfilename != None:
            self.addannotations(annotationfilename)


    def addannotations(self, annotationfilename):
        """
        Read brat text file and annotations
        :param annotationfilename: name of brat annotation file in xml format
        """
        # create tree, get root, then parse through mentions and annotations and build the group models
        self.annotations = []
        self.groupmodels = []
        tree = ET.parse(annotationfilename)
        root = tree.getroot()
        for child in root:
            if child.tag=='Mention':
                self.annotations.append(MentionAnnotation(child.attrib['id'], child.attrib['label'], 
                                                          child.attrib['span'], child.attrib['str']))
            elif child.tag=="Group":
                self.annotations.append(GroupAnnotation(child.attrib['id'], child.attrib['type'], 
                                                        child.attrib['typeid'], child.attrib['member']))
            elif child.tag!='Text':
                raise ValueError("Invalid xml element "+str(child.tag))
        self.__build_group_models__()


    def allmentions(self):
        """ Return a set holding all mentions
        :returns set of mention annotations
        """
        return set([m for m in self.annotations if isinstance(m, MentionAnnotation)])

    def allgroups(self):
        """ Return a set holding all group annotations
        :returns set of group annotations
        """
        return set([m for m in self.annotations if isinstance(m, GroupAnnotation)])

    def mention_by_id(self, mid):
        """ return a mention by id """
        for m in self.allmentions():
            if m.maid == mid:
                return m
        return None

    def mentions_by_types(self, mtype):
        """ Return a set holding all mentions
        :param mtype: a string holding the mention type to return
        :returns set of mention annotations
        """
        return set([m for m in self.annotations if (isinstance(m, MentionAnnotation) and (m.matype == mtype))])

    def mentionids(self):
        """
        Get a list of mention ids
        :return: set of mention ids
        """
        return set([m.maid for m in self.annotations if isinstance(m, MentionAnnotation)])

    def mentiontypes(self):
        """
        Get a list of mention types
        :return: set of mention types
        """
        return set([m.matype for m in self.annotations if isinstance(m, MentionAnnotation)])

    def allgroupmodels(self):
        """ return a set of all group models """
        return set(self.groupmodels)


    def len_locs(self):
        """ return the total length of mention annotations """
        lsum=0.0
        for i in range(0,len(self.malocs)):
            lsum += self.malocs[i][1]-self.malocs[i][0]
        return lsum

    def find_mention_ignore_id(self, inm):
        """ find a mention that matches the input mention ignoring only the id """
        for ann in self.annotations:
            if ((isinstance(ann,MentionAnnotation)) and (ann.matype==inm.matype) and (ann.matext==inm.matext) and len(ann.malocs)==len(inm.malocs)):
                locsmatch=True
                for i in range(0,len(ann.malocs)):
                    if ((ann.malocs[i][0]!=inm.malocs[i][0]) or (ann.malocs[i][1]!=inm.malocs[i][1])):
                        locsmatch=False
                        break
                if locsmatch==True:
                    return ann
        return None



    def write(self, filename):
        """ write out to file """
        with open(filename, "w") as f:
            f.write(str(self) + "\n")

    def __build_group_models__(self):
        """ rebuild the group models """
        # iterate through group annotations building up group models as we go
        gmodels={}
        for ga in self.allgroups():
            groupid=ga.gatype+"-"+ga.gatypeid

            if groupid in gmodels:
                gm=gmodels[groupid]
            else:
                gm=GroupModel(groupid, ga.gatype)
                gmodels[groupid]=gm
            gm.mentions.append(self.mention_by_id(ga.gamention))
        self.groupmodels=list(gmodels.values())


    def __str__(self):
        s = ""
        for an in self.annotations:
            s = '\n'.join([s, str(an)])
        for an in self.groupmodels:
            s = '\n'.join([s, str(an)])
        return s


