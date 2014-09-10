""" Caching
"""
import logging
from DateTime import DateTime
logger = logging.getLogger("eea.pdf")

def cacheKey(method, self, *args, **kwargs):
    """ Generate unique cache id
    """
    name = getattr(self, '__name__', '')
    return ':'.join((self.context.absolute_url(1), name))

def _updateBackRefs(obj, evt):
    """ Update back-refs modification date
    """
    getBRefs = getattr(obj, 'getBRefs', lambda: [])
    for item in getBRefs():
        setModificationDate = getattr(
            item, 'setModificationDate', lambda modification_date: None)
        setModificationDate(DateTime())

def updateBackRefs(obj, evt):
    """ Safely update back-refs modification date
    """
    try:
        _updateBackRefs(obj, evt)
    except Exception, err:
        logger.exception(err)
