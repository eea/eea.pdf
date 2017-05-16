""" Schema extender
"""
from Products.Archetypes.Widget import ImageWidget
from Products.Archetypes.Widget import FileWidget
from Products.Archetypes.utils import IntDisplayList
from Products.Archetypes import public
from plone.app.blob.field import ImageField
from plone.app.blob.field import FileField
from zope.interface import implements
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


class ExtendedFileField(ExtensionField, FileField):
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

        ExtendedIntegerField('tocdepth',
           schemata='settings',
           default=4,
           write_permission="Can customize PDF",
           widget=public.SelectionWidget(
               label=_(u"Table of contents depth level"),
               description=_(
                   u"Which header tags should be taken into "
                   u"consideration for the table of contents."
               )
           ),
           vocabulary=IntDisplayList([(0, 'TOC Disabled'),
                                      (1, 'H1'), (2, 'H1,H2'),
                                      (3, 'H1,H2,H3'),
                                      (4, 'H1,H2,H3,H4')])
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

        ExtendedFileField(
            name='pdfStatic',
            schemata='settings',
            write_permission="Can customize PDF",
            widget=FileWidget(
                label=_(u"PDF static"),
                description=_(
                    u"Upload custom pdf bypassing the dynamically generated pdf"
                )
            )
        ),

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
                    u"Maximum children items to include "
                    u"while generating PDF for collection "
                    u"or folderish content-types where object is collection or "
                    u"folderish. Leave it empty to use the portal "
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
