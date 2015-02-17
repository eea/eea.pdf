""" Events
"""
from eea.converter.interfaces import IExportFail, IExportSuccess
from eea.converter.interfaces import IAsyncExportFail, IAsyncExportSuccess

class IPDFExportSuccess(IExportSuccess):
    """ PDF export succeeded
    """

class IPDFExportFail(IExportFail):
    """ PDF export failed
    """

class IAsyncPDFExportSuccess(IAsyncExportSuccess):
    """ Async job for PDF export succeeded
    """

class IAsyncPDFExportFail(IAsyncExportFail):
    """ Async job for PDF export failed
    """
