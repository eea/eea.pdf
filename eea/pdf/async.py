""" Async jobs
"""
import os
import logging
logger = logging.getLogger('eea.pdf')

class PDFConversionError(IOError):
    """ PDF conversion error
    """
    def __init__(self, *args, **kwargs):
        super(PDFConversionError, self).__init__(*args, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

def make_async_pdf(context, converter, **kwargs):
    """ Async job
    """
    email = kwargs.get('email', '')
    filepath = kwargs.get('filepath', '')

    if not filepath:
        raise PDFConversionError('Invalid filepath for output PDF', email=email)

    converter.run()

    if not converter.path:
        raise PDFConversionError('Invalid output PDF', email=email)

    converter.copy(converter.path, filepath)
    converter.cleanup()

    return kwargs

def job_failure_callback(failure, **kwargs):
    """ Async job failed
    """
    error = getattr(failure, 'value', None)
    email = getattr(error, 'email', kwargs.get('email', ''))
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
