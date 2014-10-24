""" PDF View
"""
import logging
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.converter.browser.app.pdfview import Cover as PDFCover
from eea.converter.browser.app.pdfview import BackCover as PDFBackCover
from eea.pdf.utils import getApplicationRoot
logger = logging.getLogger('eea.pdf')

class Cover(PDFCover):
    """ Custom PDF cover
    """
    template = ViewPageTemplateFile('cover.pt')

    @property
    def header(self):
        """ Cover header
        """
        doc = getApplicationRoot(self.context)
        return doc.title_or_id()

    @property
    def themes(self):
        """ Get object themes
        """
        themes = queryMultiAdapter((self.context, self.request),
                                   name='themes-object')
        if not themes:
            return
        for theme in themes.items():
            theme = themes.item_to_short_dict(theme)
            image = theme.get('image', None)
            if not image:
                continue
            theme['image'] = image.replace('/image_icon', '/image_preview')
            yield theme

    def truncate(self, text, length=70, orphans=10,
                 suffix=u".", end=u".", cut=False):
        """ Custom truncate
        """
        return super(Cover, self).truncate(text, length, orphans,
                                           suffix, end, cut)

class BackCover(PDFBackCover):
    """ PDF Back cover
    """
