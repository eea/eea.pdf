""" Subtyping interfaces
"""
from zope.interface import Interface

class IPDFAware(Interface):
    """ Objects which can downloaded as PDF.
    """

__all__ = [
    IPDFAware.__name__,
]
