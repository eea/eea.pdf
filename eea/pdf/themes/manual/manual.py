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

        node_objects = []
        parent_brains = self.context.aq_parent.getFolderContents()
        for brain in parent_brains:
            if brain.getObject() == self.context:
                node_object = brain.getObject()
                html = self.get_node_html(node_object=node_object)
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

    def html_item(self, title="", description="", item_type="", depth=1):
        """ Returns html containing item title and description
        """
        html_title = "<h" + str(depth) + " class='" + item_type + \
            "-title'>" + title + "</h" + str(depth) + ">"

        html_description = "<div class='" + item_type + "-description'>" + \
            description + "</div>"

        html = html_title + html_description
        return html

    def get_node_children(self, node_object=None):
        """ Returns brains objects list with children of given node
        """
        node_title = node_object.Title()

    def get_node_html(self, node_object=None, depth=1, parent_html=""):
        """ Returns html containing manual title and description
        """
        node_title = node_object.Title()
        node_type = "manual"  # or section, leaf-page, other
        node_depth = 1

        try:
            # Leaf page
            node_description = node_object.getText()
        except Exception:
            try:
                # Section, Manual
                node_description = node_object.Description()
            except Exception:
                # Other
                node_description = ""

        node_html = self.html_item(
            title=node_title, description=node_description,
            item_type=node_type, depth=node_depth)

        node_children = node_object.getFolderContents()

        for node_child in node_children:
            node_html = node_html + self.get_node_html(
                node_object=node_child.getObject(),
                parent_html=node_html)

        return node_html

    def __call__(self, **kwargs):
        self.update(**kwargs)
        return self.template()
