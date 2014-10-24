""" PDF View
"""
import logging
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
