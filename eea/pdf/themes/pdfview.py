""" PDF View
"""
import logging
from zope.component import queryUtility
from eea.converter.browser.app.download import Pdf as PDFDownload
from eea.converter.pdf.adapters import BodyOptionsMaker as PDFBodyOptionsMaker
from eea.pdf.interfaces import IPDFTool
logger = logging.getLogger('eea.pdf')

class Mixin(object):
    """ Mixin Utility
    """
    @property
    def theme(self):
        """ Get associated theme
        """
        theme = getattr(self, '_theme', None)
        if theme is not None:
            return self._theme

        ptool = queryUtility(IPDFTool)
        ptype = getattr(self.context, 'portal_type', '')
        themes = getattr(ptool, 'themes', lambda: [])
        for theme in themes():
            field = theme.getField('types')
            types = field.getAccessor(theme)()
            if ptype in types:
                self._theme = theme
                return self._theme

        default = getattr(ptool, 'default', lambda: None)
        self._theme = default()
        return self._theme

    def getValue(self, name, default=''):
        """ Get theme based options
        """
        theme = self.theme
        if not theme:
            return default

        field = theme.getField(name)
        if not field:
            return default

        accessor = field.getAccessor(theme)
        if not accessor:
            return default

        return accessor()

    def getTemplate(self, name, default=None):
        """ Get template by name
        """
        template = self.getValue(name)
        if not template:
            return default
        return self.context.restrictedTraverse(template, default)


class BodyOptionsMaker(PDFBodyOptionsMaker, Mixin):
    """ Custom PDF options maker
    """
    @property
    def body(self):
        """ Safely get pdf.body
        """
        if not self.theme:
            return super(BodyOptionsMaker, self).body

        if self._body is None:
            template = self.getValue('body')
            self._body = ('/'.join((self.context.absolute_url(), template))
                            if template else '')
        return self._body

    @property
    def header(self):
        """ Safely get pdf.header
        """
        if not self.theme:
            return super(BodyOptionsMaker, self).header

        if self._header is None:
            template = self.getValue('header')
            self._header = ('/'.join((self.context.absolute_url(), template))
                            if template else '')
        return self._header

    @property
    def footer(self):
        """ Safely get pdf.footer
        """
        if not self.theme:
            return super(BodyOptionsMaker, self).footer

        if self._footer is None:
            template = self.getValue('footer')
            self._footer = ('/'.join((self.context.absolute_url(), template))
                            if template else '')
        return self._footer
