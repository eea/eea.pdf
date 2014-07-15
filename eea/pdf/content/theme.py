""" EEA Relations Content Type
"""
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder

from eea.pdf.content.interfaces import IPDFTheme
from eea.pdf.config import EEAMessageFactory as _

EditSchema = atapi.Schema((
    atapi.StringField('cover',
        schemata='default',
        default='pdf.cover',
        widget=atapi.StringWidget(
            label=_(u"Cover"),
            description=_(
                u"A page template to be used for PDF Cover. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.StringField('disclaimer',
        schemata='default',
        default='pdf.disclaimer',
        widget=atapi.StringWidget(
            label=_(u"Disclaimer"),
            description=_(
                u"A page template to be used for PDF Disclaimer, "
                u"the first page after PDF cover. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.StringField('body',
        schemata='default',
        default='pdf.body',
        widget=atapi.StringWidget(
            label=_(u"Body"),
            description=_(
                u"A page template to be used for PDF Body. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.StringField('backcover',
        schemata='default',
        default='pdf.cover.back',
        widget=atapi.StringWidget(
            label=_(u"Back Cover"),
            description=_(
                u"A page template to be used for PDF Back Cover. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.StringField('header',
        schemata='default',
        default='pdf.header',
        widget=atapi.StringWidget(
            label=_(u"Header"),
            description=_(
                u"A page template to be used for PDF Header. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.StringField('footer',
        schemata='default',
        default='pdf.footer',
        widget=atapi.StringWidget(
            label=_(u"Footer"),
            description=_(
                u"A page template to be used for PDF Footer. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.StringField('toc',
        schemata='default',
        default='pdf.toc',
        widget=atapi.StringWidget(
            label=_(u"Table of contents"),
            description=_(
                u"An XSL page template to be used for PDF Table of contents. "
                u"Leave empty to disable it."
            )
        )
    ),
    atapi.BooleanField('toclinks',
       schemata='default',
       default=False,
       widget=atapi.BooleanWidget(
           label=_(u"Table of contents links"),
           description=_(u"Enable table of contents links")
       )
    ),
    atapi.IntegerField('timeout',
        schemata='default',
        default=60,
        widget=atapi.IntegerWidget(
            label=_(u"Timeout"),
            description=_(
                u"Abort PDF export after specified number of seconds. "
                u"Use zero to disable it."
            )
        )
    ),
    atapi.IntegerField('offset',
        schemata='default',
        default=0,
        widget=atapi.IntegerWidget(
            label=_(u"Offset"),
            description=_(
                u"Page numbering offset within PDF Body"
            )
        )
    ),
    atapi.LinesField('types',
         schemata='default',
         vocabulary_factory='plone.app.vocabularies.ReallyUserFriendlyTypes',
         multiValued=1,
         widget=atapi.MultiSelectionWidget(
             format='checkbox',
             label=_(u'Portal types'),
             description=_(
                 u"Use this PDF Theme for the following Portal-Types"
             )
         )
    ),
    atapi.ImageField("image",
        schemata="default",
        sizes=None,
        widget=atapi.ImageWidget(
            label=_("Preview"),
            description=_("Upload a preview image for this theme")
        )
    ),
))

class PDFTheme(ATFolder):
    """ PDF Theme
    """
    implements(IPDFTheme)
    portal_type = meta_type = 'PDFTheme'
    archetypes_name = 'EEA PDF Theme'
    _at_rename_after_creation = True
    schema = ATFolder.schema.copy() + EditSchema.copy()
    schema['description'].widget.modes = ()
