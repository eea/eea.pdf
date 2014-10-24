""" PDF View
"""
from eea.converter.browser.app.pdfview import Toc as PDFToc
from eea.pdf.themes.pdfview import Mixin

class Toc(PDFToc, Mixin):
    """ Custom PDF Table of Contents
    """
    def __init__(self, context, request):
        super(Toc, self).__init__(context, request)
        self._toc_links = None

    @property
    def toc_links(self):
        """ Enable or disable table of contents links
        """
        if not self.theme:
            return super(Toc, self).toc_links

        if self._toc_links is None:
            self._toc_links = self.getValue('toclinks', None)
        return self._toc_links

    @property
    def header(self):
        """ i18n header
        """
        self.request.alwaysTranslate = True
        text = self.context.translate(u"Contents", domain="eea")
        return text
