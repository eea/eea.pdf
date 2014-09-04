""" Async jobs
"""
import errno
import os
import logging
from zope import event
from eea.pdf.events.async import AsyncPDFExportFail, AsyncPDFExportSuccess
logger = logging.getLogger('eea.pdf')

class PDFConversionError(IOError):
    """ PDF conversion error
    """

def make_async_pdf(context, converter, **kwargs):
    """ Async job
    """
    filepath = kwargs.get('filepath', '')
    url = kwargs.get('url', '')

    if not filepath:
        converter.cleanup()
        event.notify(AsyncPDFExportFail(context, **kwargs))
        raise PDFConversionError(2, 'Invalid filepath for output PDF', url)

    # Maybe a previous async job already generated our PDF
    if file_exists(filepath):
        event.notify(AsyncPDFExportSuccess(context, **kwargs))
        return

    try:
        converter.run(safe=False)
    except Exception, err:
        event.notify(AsyncPDFExportFail(context, **kwargs))
        errno = getattr(err, 'errno', 2)
        raise PDFConversionError(errno, err, url)

    if not converter.path:
        converter.cleanup()
        event.notify(AsyncPDFExportFail(context, **kwargs))
        raise PDFConversionError(2, 'Invalid output PDF', url)

    converter.copy(converter.path, filepath)
    converter.cleanup()

    event.notify(AsyncPDFExportSuccess(context, **kwargs))

def file_exists(path):
    """ File on disk and is non-empty
    """
    if os.path.exists(path) and os.path.getsize(path):
        return True
    return False
