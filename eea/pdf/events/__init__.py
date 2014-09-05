""" Events
"""
from zope.interface import implementer
from eea.pdf.events.interfaces import IPDFEvent, IAsyncPDFEvent

@implementer(IPDFEvent)
class PDFEvent(object):
    """ Abstract PDF event
    """
    def __init__(self, context, **kwargs):
        self.object = context

@implementer(IAsyncPDFEvent)
class AsyncPDFEvent(PDFEvent):
    """ Abstract PDF event for all async PDF events
    """
