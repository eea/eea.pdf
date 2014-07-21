""" Subtyping interfaces
"""
from zope.interface import Interface

class IPDFAware(Interface):
    """ Objects which can be downloaded as PDF.
    """

class ICollectionPDFAware(IPDFAware):
    """ Collections of objects which can be downloaded as PDF.
    """
