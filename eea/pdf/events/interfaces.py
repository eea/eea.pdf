""" Events
"""

from zope.component.interfaces import IObjectEvent

class IPDFEvent(IObjectEvent):
    """ Base Event Interface for all PDF events
    """

class IPDFExportSuccess(IPDFEvent):
    """ PDF export succeeded
    """

class IPDFExportFail(IPDFEvent):
    """ PDF export failed
    """

class IAsyncPDFEvent(IPDFEvent):
    """ Base Event Interface for all Async PDF events
    """

class IAsyncPDFExportSuccess(IAsyncPDFEvent):
    """ Async job for PDF export succeeded
    """

class IAsyncPDFExportFail(IAsyncPDFEvent):
    """ Async job for PDF export failed
    """
