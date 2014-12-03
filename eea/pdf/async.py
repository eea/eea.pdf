""" Async jobs
"""
import os
import logging
from kv import KV
import tempfile
from Acquisition import Implicit
from zope import event
from zope.interface import implementer
from eea.pdf.events.interfaces import IPDFContextWrapper
from eea.pdf.events.async import AsyncPDFExportFail, AsyncPDFExportSuccess
from eea.converter.config import TMPDIR
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
    filepath_lock = filepath + '.lock'
    filepath_meta = filepath + '.meta'

    url = kwargs.get('url', '')
    email = kwargs.get('email', '')

    wrapper = ContextWrapper(context)(**kwargs)

    if not filepath:
        wrapper.error = 'Invalid filepath for output PDF'
        converter.cleanup()

        event.notify(AsyncPDFExportFail(wrapper))
        raise PDFConversionError(2, 'Invalid filepath for output PDF', url)

    # Maybe another async worker is generating our PDF. If so, we update the
    # list of emails where to send a message when ready and free this worker.
    # The already running worker will do the job for us.
    if os.path.exists(filepath_lock) and os.path.exists(filepath_meta):
        update_emails(filepath_meta, email)
        converter.cleanup()
        return

    # Maybe a previous async job already generated our PDF
    if file_exists(filepath):
        converter.cleanup()
        event.notify(AsyncPDFExportSuccess(wrapper))
        return

    # Mark the begining of the convertion
    with tempfile.NamedTemporaryFile(
            prefix='eea.pdf.', suffix='.lock',
            dir=TMPDIR(), delete=False) as ofile:
        lock = ofile.name

    converter.copy(lock, filepath_lock)
    converter.toclean.add(filepath_lock)
    converter.toclean.add(lock)

    # Share some metadata with other async workers
    with tempfile.NamedTemporaryFile(
            prefix='eea.pdf.', suffix='.meta',
            dir=TMPDIR(), delete=False) as ofile:
        meta = ofile.name

    converter.copy(meta, filepath_meta)
    converter.toclean.add(filepath_meta)
    converter.toclean.add(meta)

    update_emails(filepath_meta, email)

    try:
        converter.run(safe=False)
    except Exception, err:
        wrapper.error = err
        wrapper.email = get_emails(filepath_meta, email)
        converter.cleanup()

        event.notify(AsyncPDFExportFail(wrapper))
        errno = getattr(err, 'errno', 2)
        raise PDFConversionError(errno, err, url)

    if not converter.path:
        wrapper.error = "Invalid output PDF"
        wrapper.email = get_emails(filepath_meta, email)
        converter.cleanup()

        event.notify(AsyncPDFExportFail(wrapper))
        raise PDFConversionError(2, 'Invalid output PDF', url)

    wrapper.email = get_emails(filepath_meta, email)
    converter.copy(converter.path, filepath)
    converter.cleanup()

    event.notify(AsyncPDFExportSuccess(wrapper))


def update_emails(filepath, email):
    """ Update metadata file with given email
    """
    email = email.strip()
    if not email:
        return

    try:
        db = KV(filepath, 'emails')
        db[email] = True
    except Exception, err:
        logger.exception(err)


def get_emails(filepath, default=''):
    """ Get emails from file comma separated if iterable is False
    """
    try:
        db = KV(filepath, 'emails')
        emails = db.keys()
    except Exception, err:
        logger.exception(err)
        return default
    return ','.join(emails)


def file_exists(path):
    """ File on disk and it's not empty
    """
    if os.path.exists(path) and os.path.getsize(path):
        return True
    return False
