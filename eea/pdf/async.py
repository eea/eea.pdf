""" Async jobs
"""
import errno
import os
import logging
from Acquisition import Implicit
from zope import event
from zope.interface import implementer
from eea.pdf.events.interfaces import IPDFContextWrapper
from eea.pdf.events.async import AsyncPDFExportFail, AsyncPDFExportSuccess
logger = logging.getLogger('eea.pdf')

class PDFConversionError(IOError):
    """ PDF conversion error
    """

@implementer(IPDFContextWrapper)
class ContextWrapper(Implicit):
    """ Context wrapper
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self.__of__(self.context)

def make_async_pdf(context, converter, **kwargs):
    """ Async job
    """
    filepath = kwargs.get('filepath', '')
    url = kwargs.get('url', '')

    wrapper = ContextWrapper(context)(**kwargs)

    if not filepath:
        converter.cleanup()
        wrapper.error = 'Invalid filepath for output PDF'
        event.notify(AsyncPDFExportFail(wrapper))
        raise PDFConversionError(2, 'Invalid filepath for output PDF', url)

    # Maybe a previous async job already generated our PDF
    if file_exists(filepath):
        event.notify(AsyncPDFExportSuccess(wrapper))
        return

    try:
        converter.run(safe=False)
    except Exception, err:
        wrapper.error = err
        event.notify(AsyncPDFExportFail(wrapper))
        errno = getattr(err, 'errno', 2)
        raise PDFConversionError(errno, err, url)

    if not converter.path:
        converter.cleanup()
        wrapper.error = "Invalid output PDF"
        event.notify(AsyncPDFExportFail(wrapper))
        raise PDFConversionError(2, 'Invalid output PDF', url)

    converter.copy(converter.path, filepath)
    converter.cleanup()

    event.notify(AsyncPDFExportSuccess(wrapper))

def file_exists(path):
    """ File on disk and is non-empty
    """
    if os.path.exists(path) and os.path.getsize(path):
        return True
    return False
