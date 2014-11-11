""" Schema extender
"""
from Products.Archetypes.Widget import ImageWidget
from plone.app.blob.field import ImageField

from zope.interface import implements
from Products.Archetypes import public
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField

from eea.pdf.config import EEAMessageFactory as _
from eea.pdf.interfaces import ILayer, IPDFTool, IPDFTheme


class ExtendedIntegerField(ExtensionField, public.IntegerField):
    """ IntegerField for schema extender
    """

class ExtendedStringField(ExtensionField, public.StringField):
    """ StringField for schema extender
    """

class ExtendedImageField(ExtensionField, ImageField):
    """ derivative of blobfield for extending schemas """


class PDFSchemaExtender(object):
    """ Schema extender
    """
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ILayer

    fields = (
        ExtendedStringField(
            name='pdfTheme',
            schemata='settings',
            default='',
            write_permission="Can customize PDF",
            vocabulary_factory='eea.pdf.vocabulary.Themes',
            widget=public.SelectionWidget(
                label=_(u"PDF Theme"),
                description=_(
                    u"Disable PDF export or override theme used to export "
                    u"this content as PDF."
                )
            )
        ),
    )

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns provenance list field
        """
        if IPDFTool.providedBy(self.context):
            return []
        if IPDFTheme.providedBy(self.context):
            return []
        return self.fields


class CollectionSchemaExtender(PDFSchemaExtender):
    """ Schema extender
    """
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ILayer

    fields = (
        ExtendedIntegerField(
            name='pdfMaxDepth',
            schemata='settings',
            write_permission="Can customize PDF",
            widget=public.IntegerWidget(
                label=_(u"PDF Maximum depth"),
                description=_(
                    u"Maximum depth to recursively include children items "
                    u"while generating PDF. Leave it empty to use the portal "
                    u"global defined value."
                )
            )
        ),
        ExtendedIntegerField(
            name='pdfMaxBreadth',
            schemata='settings',
            write_permission="Can customize PDF",
            widget=public.IntegerWidget(
                label=_(u"PDF Maximum breadth"),
                description=_(
                    u"Maximum breadth to include children items "
                    u"while generating PDF. Leave it empty to use the portal "
                    u"global defined value."
                )
            )
        ),
        ExtendedIntegerField(
            name='pdfMaxItems',
            schemata='settings',
            write_permission="Can customize PDF",
            widget=public.IntegerWidget(
                label=_(u"PDF Maximum items"),
                description=_(
                    u"Total maximum children items to be included"
                    u"while generating PDF. Leave it empty to use the portal "
                    u"global defined value."
                )
            )
        ),
        ExtendedImageField(
            name='coverImage',
            schemata='settings',
            write_permission="Can customize PDF",
            widget=ImageWidget(
                label=_(u"PDF cover main image"),
                description=_(
                    u"Main cover image that will show up on the pdf cover page"
                )
            )
        ),
    )
