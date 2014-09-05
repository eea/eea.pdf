""" Download PDF
"""
import logging
from zope import event
from zope.publisher.interfaces import NotFound
from zope.component import queryMultiAdapter, queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.async.interfaces import IAsyncService
from eea.converter.browser.app.download import Pdf
from eea.downloads.interfaces import IStorage
from eea.pdf.config import EEAMessageFactory as _
from eea.pdf.events.sync import PDFExportFail, PDFExportSuccess
from eea.pdf.events.async import AsyncPDFExportSuccess
from eea.pdf import async
logger = logging.getLogger('eea.pdf')

class Download(Pdf):
    """ Download PDF
    """
    template = ViewPageTemplateFile('../zpt/download.pt')

    def make_pdf(self, dry_run=False, **kwargs):
        """ Compute pdf
        """
        data = super(Download, self).make_pdf(dry_run=dry_run, **kwargs)

        # Async
        if dry_run:
            return data

        # Sync events
        if not data:
            event.notify(PDFExportFail(self.context))
        event.notify(PDFExportSuccess(self.context))

        return data

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
        # PDF already generated
        storage = IStorage(self.context).of('pdf')
        filepath = storage.filepath()
        fileurl = storage.absolute_url()

        if async.file_exists(filepath):
            wrapper = async.ContextWrapper(self.context)(
                fileurl=fileurl,
                filepath=filepath,
                email=email,
                url=self.context.absolute_url()
            )

            event.notify(AsyncPDFExportSuccess(wrapper))
            return self.finish()

        # Cheat condition @@plone_context_state/is_view_template
        self.request['ACTUAL_URL'] = self.context.absolute_url()

        # Async generate PDF
        converter = self.make_pdf(dry_run=True)
        worker = queryUtility(IAsyncService)
        worker.queueJob(
            async.make_async_pdf,
            self.context, converter,
            email=email,
            filepath=filepath,
            fileurl=fileurl,
            url=self.context.absolute_url(),
            # environ=getattr(self.request, 'environ', {})
        )

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

        # Check for permission
        if not getattr(support, 'can_download', lambda: False)():
            raise NotFound(self.context, self.__name__, self.request)

        # Don't download PDF asynchronously
        if not support.async():
            return super(Download, self).__call__(**kwargs)

        # We have the email, continue
        email = getattr(support, 'email', lambda: None)()
        if email:
            return self.download(email, **kwargs)

        # Email provided
        if self.request.method.lower() == 'post':
            return self.post(**kwargs)

        # Ask for email
        return self.template()
