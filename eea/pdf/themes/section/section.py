""" PDF View
"""
from zope.component import queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from eea.pdf.interfaces import IPDFTool


class Body(BrowserView):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("section.body.pt")

    def __init__(self, context, request):
        super(Body, self).__init__(context, request)
        self._macro = 'content-core'
        self._theme = None
        self._maxdepth = None
        self._maxbreadth = None
        self._maxitems = None
        self._depth = 0
        self._count = 1

    def theme(self, context=None):
        """ PDF Theme
        """
        tool = queryUtility(IPDFTool)
        res_theme = None
        try:
            res_theme = tool.theme(context)
        except Exception:
            pass

        if res_theme is None:
            try:
                res_theme = tool.theme(self.context)
            except Exception:
                pass

        return res_theme

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
        return self.context.getFolderContents()

    @property
    def pdfs(self):
        """ Section children
        """
        self._depth += 1
        if self.depth > self.maxdepth:
            return

        ajax_load = self.request.get('ajax_load', False)
        self.request.form['ajax_load'] = True

        # Section info (title + description)
        parent_brains = self.context.aq_parent.getFolderContents()
        for brain in parent_brains:
            if brain.getObject() == self.context:
                doc = brain.getObject()
                theme = self.theme(doc)
                body = getattr(theme, 'body', '')
                if not body:
                    continue
                if isinstance(body, unicode):
                    body = body.encode('utf-8')

                try:
                    pdf = doc.restrictedTraverse(body)
                    self._count += 1

                    section_title = self.context.Title()
                    section_description = self.context.Description()

                    html_title = "<h1 class='section-title'>" + \
                        section_title + "</h1>"

                    html_description = "<div class='section-description'>" + \
                        section_description + "</div>"

                    html = html_title + html_description

                except Exception:
                    continue
                else:
                    self._count = getattr(pdf, 'count', self._count)
                    yield html

        # Leaf pages (title + html)
        for brain in self.brains:
            if self.count > self.maxitems:
                break

            doc = brain.getObject()
            theme = self.theme(doc)
            body = getattr(theme, 'body', '')
            if not body:
                continue
            if isinstance(body, unicode):
                body = body.encode('utf-8')

            try:
                pdf = doc.restrictedTraverse(body)
                self._count += 1

                html = pdf(
                    macro=self.macro,
                    maxdepth=self.maxdepth,
                    maxbreadth=self.maxbreadth,
                    maxitems=self.maxitems,
                    depth=self.depth,
                    count=self.count
                )

                title = pdf.context.title
                html_title = "<h1>" + title + "</h1>"

                html = html_title + html

            except Exception:
                continue
            else:
                self._count = getattr(pdf, 'count', self._count)
                yield html

        self.request.form['ajax_load'] = ajax_load

    def update(self, **kwargs):
        """ Update counters
        """
        kwargs.update(self.request)
        self._macro = kwargs.get('macro', self._macro)
        self._maxdepth = kwargs.get('maxdepth', None)
        self._maxbreadth = kwargs.get('maxbreadth', None)
        self._maxitems = kwargs.get('maxitems', None)
        self._depth = kwargs.get('depth', self._depth)
        self._count = kwargs.get('count', self._count)

    def __call__(self, **kwargs):
        self.update(**kwargs)
        return self.template()
