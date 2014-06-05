""" PDF View
"""
import logging
from zope.component import queryUtility
from eea.converter.browser.app.download import Pdf as PDFDownload
from eea.converter.pdf.adapters import OptionsMaker as PDFOptionsMaker
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


class OptionsMaker(PDFOptionsMaker, Mixin):
    """ Custom PDF options maker
    """
    def __init__(self, context):
        super(OptionsMaker, self).__init__(context)
        self._header = None
        self._footer = None

    @property
    def header(self):
        """ Safely get pdf.header
        """
        if not self.theme:
            return super(OptionsMaker, self).header

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
            return super(OptionsMaker, self).footer

        if self._footer is None:
            template = self.getValue('footer')
            self._footer = ('/'.join((self.context.absolute_url(), template))
                            if template else '')
        return self._footer

    def getOptions(self):
        """ Custom options
        """
        if not self.theme:
            return super(OptionsMaker, self).getOptions()

        options = super(OptionsMaker, self).getOptions()
        offset = self.getValue('offset', 3)
        options['page-offset'] = repr(offset)
        return options


class Download(PDFDownload, Mixin):
    """ Custom PDF Download
    """
    def __init__(self, context, request):
        super(Download, self).__init__(context, request)
        self._cover = None
        self._body = None
        self._backcover = None
        self._disclaimer = None

    @property
    def cover(self):
        """ PDF cover page
        """
        if not self.theme:
            return super(Download, self).cover

        if not self._cover:
            # pdf.print.css requirement
            self.request.URL0 = self.getValue('cover')
            self._cover = self.getTemplate('cover')
        return self._cover

    @property
    def disclaimer(self):
        """ PDF disclaimer
        """
        if not self.theme:
            return super(Download, self).disclaimer

        if not self._disclaimer:
            self._disclaimer = self.getTemplate('disclaimer')
        return self._disclaimer

    @property
    def body(self):
        """ PDF body
        """
        if not self.theme:
            return super(Download, self).body

        if not self._body:
            self._body = self.getTemplate('body')
        return self._body

    @property
    def backcover(self):
        """ Back cover
        """
        if not self.theme:
            return super(Download, self).backcover

        if not self._backcover:
            self._backcover = self.getTemplate('backcover')
        return self._backcover
