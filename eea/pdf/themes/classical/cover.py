""" PDF View
"""
import logging
from bs4 import BeautifulSoup
from zope.component import queryMultiAdapter
from eea.converter.browser.app.pdfview import Cover as PDFCover
from eea.pdf.utils import getApplicationRoot
logger = logging.getLogger('eea.pdf')

class Cover(PDFCover):
    """ Custom PDF cover
    """
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

    def fix_relatedItems(self, html):
        """ Remove relatedItems
        """
        soup = BeautifulSoup(html)
        for relatedItems in soup.find_all(id='relatedItems'):
            relatedItems.extract()
        return soup.find_all('html')[0].decode()

    def fix_portalMessages(self, html):
        """ Remove portal messages
        """
        soup = BeautifulSoup(html)
        for portalMessage in soup.find_all('p', {'class': 'portalMessage'}):
            portalMessage.extract()
        return soup.find_all('html')[0].decode()

    def truncate(self, text, length=300, orphans=10, suffix=u".", end=u"."):
        """ Custom truncate
        """
        title = self.context.Title()
        rows = len(title) / 65

        rowLength = length / 4
        length = length - rowLength * rows

        return super(Cover, self).truncate(text, length, orphans, suffix, end)

    def __call__(self, **kwargs):
        html = super(Cover, self).__call__(**kwargs)
        try:
            html = self.fix_relatedItems(html)
            html = self.fix_portalMessages(html)
        except Exception, err:
            logger.exception(err)
        return html
