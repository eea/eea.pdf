""" Custom behavior
"""
from zope.interface import implements
from zope import schema
from zope.component import adapts
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from eea.cache.browser.app.edit import SettingsForm
from eea.pdf.interfaces import ILayer, IPDFAware
from eea.pdf.config import EEAMessageFactory as _
from eea.pdf.cache.cache import updateBackRefs
from eea.pdf.cache.cache import updateContext
from eea.pdf.cache.cache import updateRelatedItems


class IExtraSettings(model.Schema):
    """ Extra settings
    """
    pdf = schema.Bool(
        title=_(u"PDF"),
        description=_(u"Invalidate latest generated PDF file"),
        required=False,
        default=False
    )


class ExtraBehavior(object):
    """ Cache Controller
    """
    implements(IExtraSettings)
    adapts(IPDFAware)

    def __init__(self, context):
        self.context = context

    @property
    def pdf(self):
        """ PDF
        """
        return False

    @pdf.setter
    def pdf(self, value):
        """ Invalidate last generated PDF?
        """
        if not value:
            return

        updateContext(self.context)

        if value.get('relatedItems'):
            updateRelatedItems(self.context)

        if value.get('backRefs'):
            updateBackRefs(self.context)


class ExtraSettings(extensible.FormExtender):
    """ Cache invalidation form extender
    """
    adapts(IPDFAware, ILayer, SettingsForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        """ Extend form
        """
        self.add(IExtraSettings, prefix="extra")
        self.move('pdf', after='varnish', prefix='extra')
