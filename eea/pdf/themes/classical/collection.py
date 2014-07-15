""" PDF View
"""
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

class Body(BrowserView):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("collection.body.pt")

    @property
    def pdfs(self):
        """ Folder children
        """
        brains = self.context.queryCatalog(batch=False)
        ajax_load = self.request.get('ajax_load', False)
        self.request.form['ajax_load'] = True

        for brain in brains:
            doc = brain.getObject()
            pdf = queryMultiAdapter((doc, self.request), name='pdf.body')
            yield pdf()

        self.request.form['ajax_load'] = ajax_load

    def __call__(self, **kwargs):
        return self.template()
