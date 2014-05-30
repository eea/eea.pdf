""" Depiction tools
"""
from zope.interface import implements
from Products.CMFCore.utils import UniqueObject
from Products.ATContentTypes.content.folder import ATFolder
from eea.pdf.content.interfaces import IPDFTool

class PDFTool(UniqueObject, ATFolder):
    """ Local utility to store and customize PDF themes
    """
    implements(IPDFTool)

    meta_type = portal_type = 'PDFTool'
    archetypes_name = 'EEA PDF Tool'
    manage_options = ATFolder.manage_options
    schema = ATFolder.schema.copy()
    _at_rename_after_creation = False

    def default(self):
        """ Default theme
        """
        for theme in self.objectValues('PDFTheme'):
            return theme
        return None

    def themes(self):
        """ Available themes
        """
        for theme in self.objectValues('PDFTheme'):
            yield theme
