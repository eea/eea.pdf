""" Async jobs
"""
import os
import logging
logger = logging.getLogger('eea.pdf')

class PDFConversionError(IOError):
    """ PDF conversion error
    """

def make_async_pdf(context, converter, **kwargs):
    """ Async job
    """
    email = kwargs.get('email', '')
    filepath = kwargs.get('filepath', '')

    if not filepath:
        converter.cleanup()
        raise PDFConversionError(2, 'Invalid filepath for output PDF', email)

    # Maybe a previous async job already generated our PDF
    if file_exists(filepath):
        return kwargs

    converter.run()
    if not converter.path:
        converter.cleanup()
        raise PDFConversionError(2, 'Invalid output PDF', email)

    converter.copy(converter.path, filepath)
    converter.cleanup()

    return kwargs

def job_failure_callback(failure, **kwargs):
    """ Async job failed
    """
    error = getattr(failure, 'value', None)
    email = getattr(error, 'filename', kwargs.get('email', ''))
    logger.warn("Failure %s", email)

def job_success_callback(result):
    """ Async job succeeded
    """
    # Avoid false success
    if not isinstance(result, dict):
        return

    # Handle success
    logger.info("Success %s", result)

def file_exists(path):
    """ File on disk and is non-empty
    """
    if os.path.exists(path) and os.path.getsize(path):
        return True
    return False
