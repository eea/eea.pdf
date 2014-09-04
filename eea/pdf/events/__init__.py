""" Events
"""
import sys
from zope.interface import implementer
from ZPublisher.HTTPResponse import HTTPResponse
from ZPublisher.HTTPRequest import HTTPRequest
from eea.pdf.events.interfaces import IPDFEvent, IAsyncPDFEvent

@implementer(IPDFEvent)
class PDFEvent(object):
    """ Abstract PDF event
    """
    def __init__(self, context, **kwargs):
        self.object = context
        # sdm = getattr(context, 'session_data_manager', None)
        sdm = None
        session = sdm.getSessionData(create=True) if sdm else None

        for key, value in kwargs.items():
            setattr(self, key, value)
            if not session:
                continue
            session.set(key, value)

        import ipdb; ipdb.set_trace()

@implementer(IAsyncPDFEvent)
class AsyncPDFEvent(PDFEvent):
    """ Abstract PDF event for all async PDF events
    """
    # def __init__(self, context, **kwargs):
    #     if not getattr(context, 'REQUEST', None):
    #         response = HTTPResponse(stdout=sys.stdout)
    #         env = kwargs.get('environ', None) or {
    #             'SERVER_NAME':'async_server',
    #             'SERVER_PORT':'80',
    #             'REQUEST_METHOD':'GET'
    #         }
    #         context.REQUEST = HTTPRequest(sys.stdin, env, response)
    #     super(AsyncPDFEvent, self).__init__(context, **kwargs)
