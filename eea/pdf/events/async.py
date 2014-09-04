""" Async events
"""

from zope.interface import implementer
from eea.pdf.events.interfaces import IAsyncPDFExportFail
from eea.pdf.events.interfaces import IAsyncPDFExportSuccess
from eea.pdf.events import AsyncPDFEvent

@implementer(IAsyncPDFExportFail)
class AsyncPDFExportFail(AsyncPDFEvent):
    """ Event triggered when an async PDF export job failed
    """

@implementer(IAsyncPDFExportSuccess)
class AsyncPDFExportSuccess(AsyncPDFEvent):
    """ Event triggered when an async PDF export job succeeded
    """
