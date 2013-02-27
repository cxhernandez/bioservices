#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2013 - EBI-EMBL
#
#  File author(s): 
#      https://www.assembla.com/spaces/bioservices/team
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://www.assembla.com/spaces/bioservices/wiki
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id: biomodels.py 141 2013-02-06 10:22:25Z cokelaer $
"""This module provides a class :class:`~BioGrid`.

.. topic:: What is BioGrid ?

    :URL: http://thebiogrid.org/
    :Service: Via the PSICQUIC class

    .. highlights::

        BioGRID is an online interaction repository with data compiled through
        comprehensive curation efforts. Our current index is version 3.2.97 and searches
        37,954 publications for 638,453 raw protein and genetic interactions from major
        model organism species. All interaction data are freely provided through our
        search index and available via download in a wide variety of standardized
        formats.

        -- From BioGrid website, Feb. 2013

"""
from bioservices import PSICQUIC
import re

__all__ = ["BioGRID"]


class Search(PSICQUIC):
    """ Class that carries out the actual search via psicquic."""

    def __init__(self, data):
        super(Search, self).__init__()

        self.data = data
        self.output = self.query("biogrid",self.data)
        self.interactors = self.interactors(self.output)

    def interactors(self, output):
        l = []
        for line in output:
            t = []
            for col in line.split("\t"):
                t += [col]
            l.append(t)
        out = []
        for element in l:
            x = (re.sub(".*:","", element[2:4][0]), re.sub(".*:","", element[2:4][1]))
            out.append(tuple(sorted(x)))
        return list(set(out))


class BioGRID(object):
    """ Interface to BioGRID.
    
    .. doctest::

      >>> from bioservices import BioGRID
      >>> b = BioGRID(query=["map2k4","akt1"],taxId = "9606")
      >>> b.biogrid.interactors

    Examples::

        b = BioGRID(query=["mtor","akt1"],taxId="9606",exP="two hybrid")
        b.biogrid.interactors

    One can also query an entire organism, by using the taxid as the query::
    
        b = BioGRID(query="6239")

    """

    def __init__(self, query=None, taxId=None, exP=None):

        self.query = query
        self.taxId = taxId
        self.exP = exP
        self.searchString = self._biogridSearch()
        self.biogrid = Search(self.searchString)

    def _biogridSearch(self, query=None, taxid = None, exp = None):
        """Creates a search string for the biogrid database.
    
        :param str query: the gene name(s). Can be a string or a list of strings.
        :param str taxid: the taxid for the organism of relevance. If None, 
            all organisms are choosen.
        :param str exp: the experimental protocol used to identify the interactions.
        :return: a search string for biogrid. """ 


        if query == None:
            query = self.query
        if taxid == None:
            taxid = self.taxId
        if exp == None:
            exp = self.exP

        asepNone = "%20AND%20None"
        if exp != None:
            exp = exp.replace(" ",asepNone[:-4])
        if isinstance(query,str):
            conStr = "%s%s" % (query,asepNone)
        else:
            conStr = "%s" % ("%20OR%20".join(query))
        if taxid != None or exp != None:
            if isinstance(query,list):
                conStr = "(%s)" % conStr
        conStr = "%s%s%s%s%s" % (conStr,asepNone[:-4],taxid,asepNone[:-4],exp)
        conStr = conStr.replace(asepNone,"")  
        return conStr
