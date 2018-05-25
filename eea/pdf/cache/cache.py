""" Caching
"""
import logging
from DateTime import DateTime
logger = logging.getLogger("eea.pdf")

def cacheKey(method, self, *args, **kwargs):
    """ Generate unique cache id
    """
    name = getattr(self, '__name__', '')
    request = getattr(self, 'request', {})
    if request.get('ajax_load'):
        return ':'.join((self.context.absolute_url(1), name, 'ajax'))
    return ':'.join((self.context.absolute_url(1), name))
#
# Back references
#
def _updateBackRefs(obj, evt):
    """ Update back-refs modification date
    """
    getBRefs = getattr(obj, 'getBRefs', lambda r: [])
    for item in getBRefs('relatesTo'):
        setModificationDate = getattr(
            item, 'setModificationDate', lambda modification_date: None)
        setModificationDate(DateTime())

def updateBackRefs(obj, evt=None):
    """ Safely update back-refs modification date
    """
    try:
        _updateBackRefs(obj, evt)
    except Exception, err:
        logger.exception(err)
#
# Related items
#
def _updateRelatedItems(obj, evt):
    """ Update related items modification date
    """
    getRelatedItems = getattr(obj, 'getRelatedItems', lambda: [])
    for item in getRelatedItems():
        setModificationDate = getattr(
            item, 'setModificationDate', lambda modification_date: None)
        setModificationDate(DateTime())

def updateRelatedItems(obj, evt=None):
    """ Safely update related items modification date
    """
    try:
        _updateRelatedItems(obj, evt)
    except Exception, err:
        logger.exception(err)
#
# Context
#
def _updateContext(obj, evt):
    """ Update context modification date
    """
    setModificationDate = getattr(
            obj, 'setModificationDate', lambda modification_date: None)
    setModificationDate(DateTime())

def updateContext(obj, evt=None):
    """ Safely update context modification date
    """
    try:
        _updateContext(obj, evt)
    except Exception, err:
        logger.exception(err)
