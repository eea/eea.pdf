""" Sync events
"""

from zope.interface import implementer
from eea.pdf.events.interfaces import IPDFExportFail
from eea.pdf.events.interfaces import IPDFExportSuccess
from eea.pdf.events import PDFEvent

@implementer(IPDFExportFail)
class PDFExportFail(PDFEvent):
    """ Event triggered when a PDF export job failed
    """

@implementer(IPDFExportSuccess)
class PDFExportSuccess(PDFEvent):
    """ Event triggered when a PDF export job succeeded
    """
