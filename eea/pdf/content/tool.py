""" Depiction tools
"""
from zope.interface import implementer
from Products.CMFCore.utils import UniqueObject
from Products.ATContentTypes.content.folder import ATFolder
from eea.pdf.content.interfaces import IPDFTool

@implementer(IPDFTool)
class PDFTool(UniqueObject, ATFolder):
    """ Local utility to store and customize PDF themes
    """
    meta_type = portal_type = 'PDFTool'
    archetypes_name = 'EEA PDF Tool'
    manage_options = ATFolder.manage_options
    schema = ATFolder.schema.copy()
    _at_rename_after_creation = False

    def themes(self):
        """ Available themes
        """
        for theme in self.objectValues('PDFTheme'):
            yield theme

    def theme(self, obj, default=None):
        """ Get associated theme
        """
        ptype = getattr(obj, 'portal_type', '')
        if not ptype:
            return default

        for theme in self.themes():
            field = theme.getField('types')
            types = field.getAccessor(theme)()
            if ptype in types:
                return theme
        return default
