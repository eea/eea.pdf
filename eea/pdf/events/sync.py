""" Sync events
"""

from zope.interface import implementer
from eea.pdf.events.interfaces import IPDFExportFail, IPDFExportSuccess
from eea.converter.events.sync import ExportFail, ExportSuccess

@implementer(IPDFExportFail)
class PDFExportFail(ExportFail):
    """ Event triggered when a PDF export job failed
    """

@implementer(IPDFExportSuccess)
class PDFExportSuccess(ExportSuccess):
    """ Event triggered when a PDF export job succeeded
    """
