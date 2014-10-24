""" PDF View
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.book.collection import Body as PDFBody

class Body(PDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("collection.body.pt")

    @property
    def brains(self):
        """ Brains
        """
        return self.context.getFolderContents()[:self.maxbreadth]
