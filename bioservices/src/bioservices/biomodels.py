# -*- python -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2011-2012 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://www.ebi.ac.uk/~cokelaer/bioservices
#
##############################################################################
"""This module provides a class :class:`~BioModels` that allows an easy access to all the BioModel service.

See http://www.ebi.ac.uk/biomodels-main/ for information about biomodels itself.

"""


from services import Service
import webbrowser
import copy



def checkId(fn):
    def wrapped(self, *args, **kwargs):
        ids = getattr(self, "modelsId")
        if args[0] in ids:
            return fn(self, *args, **kwargs)
        else:
            raise ValueError("""
    Id provided is not a valid ID. See modelsId attribute.""")
    return wrapped

class BioModels(Service):
    """Interface to the KEGG database

    ::


    """
    def __init__(self, verbose=True, debug=False, url=None):
        """Constructor

        :param bool verbose:
        :param bool debug:
        :param str url: redefine the wsdl URL 

        """
        if url == None:
            url = "http://www.ebi.ac.uk/biomodels-main/services/BioModelsWebServices?wsdl"
        super(BioModels, self).__init__(name="BioModels", url=url, verbose=verbose)

        self._modelsId = None



    def __len__(self):
        l = len(self.serv.getAllModelsId())
        return l


    def getAllModelsId(self):
        """Retrieves the identifiers of all published models

        :return: list of models identifiers


        ::

            >>> b.getAllModelsId()

        """
        return self.serv.getAllModelsId()

    def _get_models_id(self):
        if self._modelsId == None:
            self._modelsId = self.serv.getAllModelsId()
        return self._modelsId
    modelsId = property(_get_models_id)


    def getAllCuratedModelsId(self):
        """Retrieves the identifiers of all published curated models

        :return: list of models identifiers


        ::

            >>> b.getAllCuratedModelsId()

        """
        return self.serv.getAllCuratedModelsId()

    def getAllNonCuratedModelsId(self):
        """Retrieves the identifiers of all published curated models

        :return: list of models identifiers
        ::

            >>> b.getAllNonCuratedModelsId()

        """
        return self.serv.getAllNonCuratedModelsId()

    @checkId
    def getModelById(self, Id):
        """This method is now deprecated! 

        Instead, please use: :meth:`getModelSBMLById`

        """
        return self.serv.getModelById(Id)

    @checkId
    def getAuthorsByModelId(self, Id):
        """Retrieves the name of the authors of the publication associated with
a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.


        :return: list of names of the publication's authors
        """
        return self.serv.getAuthorsByModelId(Id)

    @checkId
    def getDateLastModifByModelId(self, Id):
        """Retrieves the date of last modification of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: date of last modification (expressed according to ISO 8601)

        .. note:: same as :meth:`getLastModifiedDateByModelId`.
        """
        return self.serv.getDateLastModifByModelId(Id)

    @checkId
    def getEncodersByModelId(self, Id):
        """Retrieves the name of the encoders of a given model.

        :return: list of names of the model's encoders
        """
        return self.serv.getEncodersByModelId(Id)

    @checkId
    def getLastModifiedDateByModelId(self, Id):
        """Retrieves the date of last modification of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: date of last modification (expressed according to ISO 8601)

        """
        return self.serv.getLastModifiedDateByModelId(Id)

    @checkId
    def getModelNameById(self, Id):
        """Retrieves the name of a model name given its identifier.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: model name

        """
        return self.serv.getModelNameById(Id)

    @checkId
    def getModelSBMLById(self, Id):
        """Retrieves the SBML form of a model (in a string) given its identifier

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: str - SBML model in a string

        ::

            >>> b = BioModels()
            >>> b.getModelSBMLById('MODEL1006230101')

        """
        return self.serv.getModelSBMLById(Id)

    @checkId
    def getModelSBMLByChEBI(self, Id):
        return self.serv.getModelSBMLByChEBI(Id)

    @checkId
    def getModelSBMLByChEBIId(self, Id):
        return self.serv.getModelSBMLByChEBIId(Id)

    @checkId
    def getPublicationByModelId(self, Id):
        """Retrieves the publication's identifier of a given model.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: publication identifier (can be a PMID, DOI or URL)
        """
        return self.serv.getPublicationByModelId(Id)

    @checkId
    def getSimpleModelByIds(self, Id):
        """Retrieves the main information about given models.

        :param str Id: a valid model Id. See :attr:`modelsId` attribute.

        :return: a XML representaton of the model meta information including
            identifier, name, publication identifierm date of last modification...
        """
        return self.serv.getSimpleModelsByIds(Id)


    def getModelsIdByPerson(self, person):
        return self.serv.getModelsIdByPerson(person)

    def getSimpleModelsByReactomeIds(self, reacID):
        """Retrieves all the models which are annotated with the given Reactome
records.

        :param: list of reactome identifiers (e.g., REACT_1590)

        :return:  models annotated with the provided Reactome identifiers, as a TreeMap (which uses Reactome identifiers as keys) 


        .. seealso:: How to retrieve REACTOME IDs in :meth:`extra_getReactomeIds`
        """
        return b.serv.getSimpleModelsByReactomeIds('REACT_1590')


    def getModelsIdByUniprotId(self, Id):
        """Retrieves all the models which are annotated with the given UniProt records.


        P12345

            >>> ID = 'BIOMD0000000033'
            >>> b.serv.getSimpleModelsByIds(ID)

        Working Uniprot Id returns the same Model (sameId) but note the
        reference. It is now a uniprot reference::

            >>> b.serv.getSimpleModelsByUniprotIds('P10113')

        The issue is to figure out the uniprot Id from the model... similarly to        the search with Reactome Id, we provide a function to retrieve Uniprot 
        Id found in the models.
    

        """
        return self.serv.getModelsIdByUniprotId(Id)

    def getModelsIdByName(self, name)
        """Retrieves the models' identifiers which name includes the given keyword.

        :param str name: 
        :return:  array of strings - list of models identifiers

        ::

            >>> b.getModelsIdByName("2009")

        """
        
        return self.serv.getModelsIdByName(name)


    def extra_getReactomeIds(self, start=0, end=1000):
        """Retrive value REACTOME Ids by scanning all Ids in a given range

        :param int start:
        :param int end:

        Search all models for reactome Ids in range REACT_start to REACT_end. 
        Can take a while.


        For instance, scanning the database for start=0 and end=3000, a list of
        106 reactome Id are returned and its takes a minute or two.
        """
        Ids = []
        for i in range(start, end):
            if i%100 == 0 and i>0:
                print("%f  done" % ((i-start)*100./float(end-start)))
            res = self.serv.getSimpleModelsByReactomeIds(['REACT_%s'%i])
            if 'REACT' in res:
                Ids.append('REACT_%s' % i)
        return Ids


    def extra_getUniprotIds(self, start=10000, end=11000):
        """Retrieve the Uniprot 


        ::
        
            >>> res = b.extra_getUniprotIds(10000,11200)
            ['P10113',
             'P10415',
             'P10523',
             'P10600',
             'P10646',
             'P10686',
             'P10687',
             'P10815',
             'P11071']
        """

        Ids = []
        for i in range(start, end):
            if i%100 == 0 and i>0:
                print("%f  done" % ((i-start)*100./float(end-start)))
            res = self.serv.getSimpleModelsByUniprotIds(['P%s'%i])
            if 'P%s' % i in res:
                Ids.append('P%s' % i)
        return Ids


todo = [
 u'getModelsIdByGO',
 u'getModelsIdByGOId',
 u'getModelsIdByName',
 u'getModelsIdByPerson',
 u'getModelsIdByPublication',
 u'getModelsIdByTaxonomy',
 u'getModelsIdByTaxonomyId',
 u'getModelsIdByUniprot',
 u'getSimpleModelsByChEBIIds',
 u'getSimpleModelsRelatedWithChEBI',
 u'getSubModelSBML',
 ]

