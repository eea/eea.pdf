""" PDF View
"""
import logging

from zope.component import queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from eea.pdf.interfaces import IPDFTool

logger = logging.getLogger("pdf_collection")


class Body(BrowserView):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("collection.body.pt")

    def __init__(self, context, request):
        super(Body, self).__init__(context, request)
        self._macro = None
        self._theme = None
        self._maxdepth = None
        self._maxbreadth = None
        self._maxitems = None
        self._depth = 0
        self._count = 1

    def theme(self, context=None):
        """ PDF Theme
        """
        if context:
            tool = queryUtility(IPDFTool)
            return tool.theme(context)

        if self._theme is None:
            tool = queryUtility(IPDFTool)
            self._theme = tool.theme(self.context)

        return self._theme

    def getValue(self, name, context='', default=None):
        """ Get value
        """
        if context == '':
            context = self.context

        getField = getattr(context, 'getField', lambda name: None)
        field = getField(name)
        if not field:
            return default

        value = field.getAccessor(context)()
        return value or default

    @property
    def macro(self):
        """ ZPT macro to use while rendering PDF
        """
        return self._macro

    @property
    def maxdepth(self):
        """ Maximum depth
        """
        if self._maxdepth is None:
            self._maxdepth = self.getValue(
                'pdfMaxDepth',
                default=self.getValue('maxdepth', self.theme(), default=0))
        return self._maxdepth

    @property
    def maxbreadth(self):
        """ Maximum breadth
        """
        if self._maxbreadth is None:
            self._maxbreadth = self.getValue(
                'pdfMaxBreadth',
                default=self.getValue('maxbreadth', self.theme(), default=0))
        return self._maxbreadth

    @property
    def maxitems(self):
        """ Maximum items
        """
        if self._maxitems is None:
            self._maxitems = self.getValue(
                'pdfMaxItems',
                default=self.getValue('maxitems', self.theme(), default=0))
        return self._maxitems

    @property
    def depth(self):
        """ Current depth
        """
        return self._depth

    @property
    def count(self):
        """ Current counter
        """
        return self._count

    @property
    def brains(self):
        """ Brains
        """
        return self.context.queryCatalog(batch=False)[:self.maxbreadth]

    def show_limit_page(self):
        """ Returns the pdf limit page
        """
        pdf = self.context.restrictedTraverse("@@pdf.limit")
        return pdf()

    @property
    def pdfs(self):
        """ Folder children
        """
        self._depth += 1
        contentish = ['Folder', 'Collection', 'Topic']
        if not self.request.get('pdf_last_brain_url'):
            brains = self.context.getFolderContents(
                contentFilter={
                    'portal_type': contentish
                })
            if brains:
                self.request['pdf_last_brain_url'] = brains[-1].getURL()
                # 31424 in case there is only one result from the content
                # filter then we need to reset the depth in order to
                # get the content of the brain
                if len(brains) == 1:
                    self._depth -= 1
        if self.depth > self.maxdepth:
            if self.context.absolute_url() == \
                    self.request.get('pdf_last_brain_url'):
                yield self.show_limit_page()
            return

        ajax_load = self.request.get('ajax_load', True)
        self.request.form['ajax_load'] = ajax_load

        for brain in self.brains:
            if self.count > self.maxitems:
                if not self.request.get('pdflimit'):
                    self.request['pdflimit'] = "reached"
                    yield self.show_limit_page()
                break

            doc = brain.getObject()
            theme = self.theme(doc)
            body = getattr(theme, 'body', '')
            if not body:
                continue

            if isinstance(body, unicode):
                body = body.encode('utf-8')
            if (self.theme(self.context).id == theme.id and
                    self.depth == self.maxdepth):
                if brain.getURL() == self.request.get('pdf_last_brain_url'):
                    if not self.request.get('pdflimit'):
                        self.request['pdflimit'] = "reached"
                        yield self.show_limit_page()
                continue
            try:
                pdf = doc.restrictedTraverse(body.split("?")[0])
                self._count += 1
                html = pdf(
                    macro=self.macro,
                    maxdepth=self.maxdepth,
                    maxbreadth=self.maxbreadth,
                    maxitems=self.maxitems,
                    depth=self.depth,
                    count=self.count
                )
            except Exception, err:
                logger.exception(err)
                continue
            else:
                self._count = getattr(pdf, 'count', self._count)
                ptype = doc.portal_type
                orig_title = doc.title
                title = orig_title if ptype in contentish else ''
                yield (title, html)

        self.request.form['ajax_load'] = ajax_load

    def update(self, **kwargs):
        """ Update counters
        """
        self._macro = kwargs.get('macro', self._macro)
        self._maxdepth = kwargs.get('maxdepth', None)
        self._maxbreadth = kwargs.get('maxbreadth', None)
        self._maxitems = kwargs.get('maxitems', None)
        self._depth = kwargs.get('depth', self._depth)
        self._count = kwargs.get('count', self._count)

    def __call__(self, **kwargs):
        kwargs.update(self.request.form)
        self.update(**kwargs)
        return self.template(**kwargs)
