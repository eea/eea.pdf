""" EEA Relations Content Type
"""
from zope.interface import implementer
from Products.Archetypes import atapi
from Products.ATContentTypes.content.folder import ATFolder
from plone.app.blob.field import ImageField
from eea.pdf.content.interfaces import IPDFTheme
from eea.pdf.config import EEAMessageFactory as _
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

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
    atapi.BooleanField('coverSubtitle',
        schemata='default',
        default=True,
        widget=atapi.BooleanWidget(
           label=_(u"Cover subtitle"),
           description=_(u"Enable display of subtitle within cover page."
                         u" By default subtitle is created from content"
                         u" description truncated to first 70 characters"
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

    atapi.BooleanField('staticFooterAndHeader',
        schemata='default',
        default=False,
        widget=atapi.BooleanWidget(
           label=_(u"Static Footer and Header"),
           description=_(u"Enable static footer and header html pages. "
                         u"Footer and header templates are evaluated once"
                         u" and then served for every pdf page."
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
    atapi.ReferenceField(
        'imagescollection',
        relationship='imagescollectionrel',
        multiValued=0,
        allowed_types=('Collection', 'ATTopic', 'Folder'),
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            label=_(u"Images cover collection"),
            description=_(u"if cover image not present use "
                           "a random cover from the collection."),
        ),
    ),
    atapi.BooleanField('javascript',
       schemata='default',
       default=True,
       widget=atapi.BooleanWidget(
           label=_(u"JavaScript"),
           description=_(u"Enable or disable javascript")
       )
    ),
    atapi.IntegerField('javascriptdelay',
       schemata='default',
       default=0,
       widget=atapi.IntegerWidget(
           label=_(u"JavaScript delay"),
           description=_(u"Wait some seconds for javascript to finish")
       )
    ),
    atapi.IntegerField('timeout',
        schemata='default',
        default=3600,
        widget=atapi.IntegerWidget(
            label=_(u"Timeout"),
            description=_(
                u"Abort PDF export after specified number of seconds. "
                u"Use zero to disable it."
            )
        )
    ),
    atapi.BooleanField('async',
        schemata='default',
        default=True,
        widget=atapi.BooleanWidget(
            label=_(u"Asynchronous"),
            description=_(
                u"Generate PDF asynchronously and send an email to the user "
                u"when it's done."
            )
        )
    ),
    atapi.IntegerField('offset',
        schemata='default',
        default=0,
        widget=atapi.IntegerWidget(
            label=_(u"Offset"),
            description=_(
                u"Page numbering offset within PDF Body."
            )
        )
    ),
    atapi.IntegerField('maxdepth',
        schemata='default',
        default=1,
        widget=atapi.IntegerWidget(
            label=_(u"Maximum depth"),
            description=_(
                u"Maximum depth to recursively include children items "
                u"while generating PDF for collection "
                u"or folderish content-types."
            )
        )
    ),
    atapi.IntegerField('maxbreadth',
        schemata='default',
        default=100,
        widget=atapi.IntegerWidget(
            label=_(u"Maximum breadth"),
            description=_(
                u"Maximum breadth to include children items "
                u"while generating PDF for collection "
                u"or folderish content-types where object is collection or "
                u"folderish."
            )
        )
    ),
    atapi.IntegerField('maxitems',
        schemata='default',
        default=1000,
        widget=atapi.IntegerWidget(
            label=_(u"Maximum items"),
            description=_(
                u"Total maximum children items to be included "
                u"while generating PDF for collection "
                u"or folderish content-types."
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
                 u"Use this PDF Theme for the following Portal-Types."
             )
         )
    ),
    ImageField("image",
        schemata="default",
        sizes=None,
        widget=atapi.ImageWidget(
            label=_(u"Preview"),
            description=_(u"Upload a preview image for this theme")
        )
    ),
))

THEME_SCHEMA = ATFolder.schema.copy() + EditSchema.copy()

def finalize_schema(schema=THEME_SCHEMA):
    """ Update schema
    """
    for field in schema.fields():
        field.write_permission = 'Manage portal'
        if field.schemata != 'default':
            field.required = False
            field.mode = 'r'

finalize_schema()

@implementer(IPDFTheme)
class PDFTheme(ATFolder):
    """ PDF Theme
    """
    portal_type = meta_type = 'PDFTheme'
    archetypes_name = 'EEA PDF Theme'
    _at_rename_after_creation = True
    schema = THEME_SCHEMA
    schema['description'].widget.modes = ()
