""" Depiction tools
"""
from zope.interface import implementer
from Products.CMFCore.utils import UniqueObject
from Products.ATContentTypes.content.folder import ATFolder
from eea.pdf.content.interfaces import IPDFTool
from eea.pdf.content.theme import finalize_schema

TOOL_SCHEMA = ATFolder.schema.copy()
finalize_schema(TOOL_SCHEMA)

@implementer(IPDFTool)
class PDFTool(UniqueObject, ATFolder):
    """ Local utility to store and customize PDF themes
    """
    meta_type = portal_type = 'PDFTool'
    archetypes_name = 'EEA PDF Tool'
    manage_options = ATFolder.manage_options
    schema = TOOL_SCHEMA
    _at_rename_after_creation = False

    def themes(self):
        """ Available themes
        """
        for theme in self.objectValues('PDFTheme'):
            yield theme

    def globalTheme(self, obj):
        """
         Get global associated theme

        :param obj: Plone object
        :return: PDFTheme object or None

        """
        ptype = getattr(obj, 'portal_type', '')
        if not ptype:
            return None

        for theme in self.themes():
            field = theme.getField('types')
            types = field.getAccessor(theme)
            if not types:
                return None
            types = types()
            if ptype in types:
                return theme
        return None

    def localTheme(self, obj):
        """
         Get locally defined theme

        :param obj: Plone object
        :return: PDFTheme object or None

        """
        getField = getattr(obj, 'getField', lambda name: None)
        field = getField('pdfTheme')
        if not field:
            return self.globalTheme(obj)

        themeName = field.getAccessor(obj)()

        # Disabled
        if themeName == '-':
            return None

        # Global defined settings
        if themeName == '':
            return self.globalTheme(obj)

        # Custom theme
        for theme in self.themes():
            if theme.getId() == themeName:
                return theme
        return self.globalTheme(obj)

    def theme(self, obj, default=None):
        """ Get defined theme for given object

        :param obj: Plone object
        :param default: return value if we can't find a theme
        :return: PDFTheme object or default

        """
        return self.localTheme(obj) or default
