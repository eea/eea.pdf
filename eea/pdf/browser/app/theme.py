""" Browser views
"""
import json
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.pdf.cache.cache import updateContext
from eea.downloads.interfaces import IStorage

class Theme(BrowserView):
    """ Custom view controller
    """
    @property
    def types(self):
        """ Types
        """
        field = self.context.getField('types')
        types = field.getAccessor(self.context)
        return types()

    def flushPDFsCache(self):
        """ Flush all PDFs cache for this theme
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        for brain in catalog.searchResults(portal_type=self.types):
            obj = brain.getObject()
            storage = IStorage(obj).of('pdf')
            storage_pdf_obj = obj.unrestrictedTraverse(
                storage.absolute_url(True), None)
            #change modification time only if
            #the object has a PDF generated in downloads
            if storage_pdf_obj is not None:
                updateContext(obj)
        return json.dumps('ok')
