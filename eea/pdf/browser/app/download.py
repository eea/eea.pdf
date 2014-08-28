""" Download PDF
"""
import logging
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from eea.converter.browser.app.download import Pdf
from eea.pdf.config import EEAMessageFactory as _
logger = logging.getLogger('eea.pdf')


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
        ## ASYNC job
        # super(Download, self).__call__(**kwargs)
        logger.warning('Download as PDF ASYNC job not started for %s',
                       self.context.absolute_url())
        return self.finish()


    def post(self, **kwargs):
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
        email = getattr(support, 'email', lambda: None)()
        if email:
            return self.download(email, **kwargs)

        if self.request.method.lower() == 'post':
            return self.post(**kwargs)

        return self.template()
