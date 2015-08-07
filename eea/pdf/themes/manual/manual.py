""" PDF View
"""
from zope.component import queryUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from eea.pdf.interfaces import IPDFTool


class Body(BrowserView):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("manual.body.pt")

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
        return self.context.getFolderContents()

    @property
    def pdfs(self):
        """ Manual children
        """
        self._depth += 1
        if self.depth > self.maxdepth:
            return

        ajax_load = self.request.get('ajax_load', False)
        self.request.form['ajax_load'] = True

        # manual title and description
        counter_a = 0
        parent_brains = self.context.aq_parent.getFolderContents()
        for brain in parent_brains:
            if brain.getObject() == self.context:
                doc_obj = brain.getObject()
                prefix = ""
                html = self.get_manual_html(
                    prefix=prefix, doc_obj=doc_obj, depth=1)
                yield html
                counter_a = counter_a + 1

        # manual sections (and leaf pages added to manual)
        for brain in self.brains:
            doc_obj = brain.getObject()
            doc_type = doc_obj.portal_type

            if doc_type == 'HelpCenterReferenceManualSection':
                # section title and description
                prefix = str(counter_a) + ". "
                html = self.get_section_html(
                    prefix=prefix, doc_obj=doc_obj, depth=2)
                yield html

                # section leaf pages
                counter_b = 1
                for brain in doc_obj.getFolderContents():
                    leaf_page_doc = brain.getObject()

                    # leaf page title and text
                    prefix = str(counter_a) + "." + str(counter_b) + ". "
                    html = self.get_leaf_page_html(
                        prefix=prefix, doc_obj=leaf_page_doc, depth=3)
                    yield html
                    counter_b = counter_b + 1

                counter_a = counter_a + 1

            elif doc_type == 'HelpCenterLeafPage':
                prefix = str(counter_a) + ". "
                html = self.get_leaf_page_html(
                    prefix=prefix, doc_obj=doc_obj, depth=2)
                yield html
                counter_a = counter_a + 1

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

    def html_item(self, prefix=None, title=None, description=None,
                  item_type=None, depth=1):
        """ Returns html containing item title and description
        """
        html_title = "<h" + str(depth) + " class='" + item_type + \
            "-title'>" + prefix + title + "</h" + str(depth) + ">"

        html_description = "<div class='" + item_type + "-description'>" + \
            description + "</div>"

        html = html_title + html_description
        return html

    def get_manual_html(self, prefix=None, doc_obj=None, depth=1):
        """ Returns html containing manual title and description
        """
        manual_title = doc_obj.Title()
        manual_description = doc_obj.Description()

        html = self.html_item(
            prefix=prefix, title=manual_title,
            description=manual_description, item_type='manual',
            depth=depth)
        return html

    def get_section_html(self, prefix=None, doc_obj=None, depth=1):
        """ Returns html containing section title and description
        """
        section_title = doc_obj.Title()
        section_description = doc_obj.Description()

        html = self.html_item(
            prefix=prefix, title=section_title,
            description=section_description,
            item_type='section', depth=depth)
        return html

    def get_leaf_page_html(self, prefix=None, doc_obj=None, depth=1):
        """ Returns html containing leaf page title and content
        """
        leaf_page_title = doc_obj.Title()
        leaf_page_description = doc_obj.getText()
        html = self.html_item(
            prefix=prefix, title=leaf_page_title,
            description=leaf_page_description,
            item_type='leaf-page', depth=depth)
        return html

    def __call__(self, **kwargs):
        self.update(**kwargs)
        return self.template()
