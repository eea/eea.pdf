""" Download PDF
"""
import sys
import logging
from pprint import pprint
from zope.interface import alsoProvides
from zope.publisher.interfaces import NotFound
from zope.component import queryMultiAdapter, queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.async.interfaces import IAsyncService
from eea.converter.browser.app.download import Pdf
from eea.downloads.interfaces import IStorage
from eea.pdf.interfaces import ILayer
from eea.pdf.config import EEAMessageFactory as _

from ZPublisher.HTTPResponse import HTTPResponse
from ZPublisher.HTTPRequest import HTTPRequest

logger = logging.getLogger('eea.pdf')

def make_async_pdf(context, converter, **kwargs):
    """ Async job
    """
    converter.run()
    storage = IStorage(context).of('pdf')
    filepath = storage.filepath()
    if converter.path:
        converter.copy(converter.path, filepath)
    converter.cleanup()
    return converter.path

def job_failure_callback(result):
    logger.exception("Failure %s", result)

def job_success_callback(result):
    logger.info("Success %s", result)

class Download(Pdf):
    """ Download PDF
    """
    template = ViewPageTemplateFile('../zpt/download.pt')

    def _redirect(self, msg=''):
        """ Redirect
        """
        if msg:
            IStatusMessage(self.request).addStatusMessage(msg, 'info')
        return self.request.response.redirect(self.context.absolute_url())

    def link(self):
        """ Download link
        """
        storage = IStorage(self.context).of('pdf')
        return storage.absolute_url()

    def cancel(self):
        """ Cancer
        """
        return self._redirect(_(u'Download canceled'))

    def finish(self):
        """ Finish download
        """
        return self._redirect(_(
            u"The PDF is being generated. "
            u"An email will be sent to you when the PDF is ready."
        ))

    def download(self, email='', **kwargs):
        """ Download
        """
        # Cheat condition @@plone_context_state/is_view_template
        self.request['ACTUAL_URL'] = self.context.absolute_url()

        converter = self.make_pdf(dry_run=True)

        async = queryUtility(IAsyncService)
        job = async.queueJob(make_async_pdf,
            self.context, converter, email=email, **kwargs
        )

        job.addCallback(job_success_callback)
        job.addCallbacks(failure=job_failure_callback)

        return self.finish()

    def post(self, **kwargs):
        """ POST
        """
        if self.request.get('form.button.cancel'):
            return self.cancel()
        elif self.request.get('form.button.download'):

            # Filter bots
            if self.request.get('body'):
                return self.finish()

            email = self.request.get('email')
            return self.download(email, **kwargs)

        return self._redirect('Invalid form')

    def __call__(self, **kwargs):
        support = queryMultiAdapter((self.context, self.request),
                                    name='pdf.support')
        if not getattr(support, 'can_download', lambda: False)():
            raise NotFound(self.context, self.__name__, self.request)

        email = getattr(support, 'email', lambda: None)()
        if email:
            return self.download(email, **kwargs)

        if self.request.method.lower() == 'post':
            return self.post(**kwargs)

        return self.template()
