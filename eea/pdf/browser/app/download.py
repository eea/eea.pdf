""" Download PDF
"""
import logging
from zope import event
from zope.publisher.interfaces import NotFound
from zope.component import queryMultiAdapter, queryUtility
from zope.component.hooks import getSite
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.async.interfaces import IAsyncService
from eea.converter.browser.app.download import Pdf
from eea.downloads.interfaces import IStorage
from eea.pdf.config import EEAMessageFactory as _
from eea.pdf.events.sync import PDFExportFail, PDFExportSuccess
from eea.pdf.events.async import AsyncPDFExportSuccess, AsyncPDFExportFail
from eea.converter.interfaces import IContextWrapper
from eea.converter import async
logger = logging.getLogger('eea.pdf')

class Download(Pdf):
    """ Download PDF
    """
    template = ViewPageTemplateFile('../zpt/download.pt')

    def __init__(self, context, request):
        super(Download, self).__init__(context, request)
        self._title = ''
        self._message = _(
            u"* The email is only used for the purpose of sending the PDF. "
            u"We do not store it for any other use."
        )
        self._email = ''
        self._link = ''

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

    @property
    def message(self):
        """ Message
        """
        return self._message

    @property
    def title(self):
        """ Title
        """
        if self._title:
            return self._title

        title = self.context.title_or_id()
        if isinstance(title, str):
            title = title.decode('utf-8')

        return _(
          u"Enter your email address where to send '${title}' PDF when ready",
            mapping={
                'title': title
            }
        )

    @property
    def email(self):
        """ User email
        """
        return self._email

    def _redirect(self, msg='', title=''):
        """ Redirect
        """
        self.request.set('disable_border', 1)
        self.request.set('disable_plone.leftcolumn', 1)
        self.request.set('disable_plone.rightcolumn', 1)
        if msg:
            self._message = msg
        if title:
            self._title = title
        return self.template()

    def link(self):
        """ Download link
        """
        if not self._link:
            storage = IStorage(self.context).of('pdf')
            self._link = storage.absolute_url()
        return self._link

    def period(self):
        """ Wait period
        """
        ptype = getattr(self.context, 'portal_type', '')
        if ptype.lower() in ('collection', 'topic', 'folder', 'atfolder'):
            return _(u"minutes")
        return _(u"seconds")

    def finish(self, email=''):
        """ Finish download
        """
        if email:
            self._email = email
            self._title = _(
                u"An email will be sent to you when the PDF is ready"
            )
            self._message = _(
                u"If you don't have access to your email address "
                u"check <a href='${link}'>this link</a> in a few ${period}.",
                mapping={
                    u"link": u"%s?direct=1" % self.link(),
                    u"period": self.period()
            })
        return self._redirect()

    def download(self, email='', **kwargs):
        """ Download
        """
        # Fallback PDF provided
        fallback = self.context.restrictedTraverse('action-download-pdf', None)
        if fallback and fallback.absolute_url().startswith(
                self.context.absolute_url()):
            self._link = self.context.absolute_url() + '/action-download-pdf'
        else:
            fallback = None

        # PDF already generated
        storage = IStorage(self.context).of('pdf')
        filepath = storage.filepath()
        fileurl = self.link()
        url = self.context.absolute_url()
        title = self.context.title_or_id()

        portal = getSite()
        from_name = portal.getProperty('email_from_name')
        from_email = portal.getProperty('email_from_address')

        if fallback or async.file_exists(filepath):
            wrapper = IContextWrapper(self.context)(
                fileurl=fileurl,
                filepath=filepath,
                email=email,
                url=url,
                from_name=from_name,
                from_email=from_email,
                title=title
            )

            event.notify(AsyncPDFExportSuccess(wrapper))
            return self.finish(email=email)

        # Cheat condition @@plone_context_state/is_view_template
        self.request['ACTUAL_URL'] = self.context.absolute_url()

        # Async generate PDF
        converter = self.make_pdf(dry_run=True)
        worker = queryUtility(IAsyncService)
        queue = worker.getQueues()['']
        worker.queueJobInQueue(queue, ('pdf',),
            async.run_async_job,
            self.context, converter,
            success_event=AsyncPDFExportSuccess,
            fail_event=AsyncPDFExportFail,
            email=email,
            filepath=filepath,
            fileurl=fileurl,
            url=url,
            from_name=from_name,
            from_email=from_email,
            title=title,
            etype='pdf'
        )

        return self.finish(email=email)

    def post(self, **kwargs):
        """ POST
        """
        if not self.request.get('form.button.download'):
            return self._redirect('Invalid form')

        email = self.request.get('email')

        # Filter bots
        if self.request.get('body'):
            return self.finish(email=email)

        if not email:
            return self.finish(email=email)

        return self.download(email, **kwargs)

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
        return self._redirect()
