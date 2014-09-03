""" Subtyping interfaces
"""
from zope.interface import Interface
from eea.converter.interfaces import ISupport

class IPDFAware(Interface):
    """ Objects which can be downloaded as PDF.
    """

class ICollectionPDFAware(IPDFAware):
    """ Collections of objects which can be downloaded as PDF.
    """

class IPDFSupport(ISupport):
    """ Custom PDF Support
    """
    def can_download():
        """ Can download PDF
        """

    def async():
        """ Download PDF asynchronously or not.
        """

    def email():
        """ Current user email
        """
