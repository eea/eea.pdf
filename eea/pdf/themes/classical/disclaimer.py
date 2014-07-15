""" PDF View
"""
import logging
from bs4 import BeautifulSoup
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.converter.browser.app.pdfview import Disclaimer as PDFDisclaimer
logger = logging.getLogger('eea.pdf')

class Disclaimer(PDFDisclaimer):
    """ Custom PDF cover
    """
    template = ViewPageTemplateFile('disclaimer.pt')

    @property
    def year(self):
        """ Publication year
        """
        published = DateTime(self.context.Date())
        return published.year()

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

    def __call__(self, **kwargs):
        html = super(Disclaimer, self).__call__(**kwargs)
        try:
            html = self.fix_relatedItems(html)
            html = self.fix_portalMessages(html)
        except Exception, err:
            logger.exception(err)
        return html
