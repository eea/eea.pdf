""" Async events
"""

from zope.interface import implementer
from eea.pdf.events.interfaces import IAsyncPDFExportFail
from eea.pdf.events.interfaces import IAsyncPDFExportSuccess
from eea.converter.events.async import AsyncExportFail, AsyncExportSuccess

@implementer(IAsyncPDFExportFail)
class AsyncPDFExportFail(AsyncExportFail):
    """ Event triggered when an async PDF export job failed
    """

@implementer(IAsyncPDFExportSuccess)
class AsyncPDFExportSuccess(AsyncExportSuccess):
    """ Event triggered when an async PDF export job succeeded
    """
