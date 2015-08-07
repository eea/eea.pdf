""" PDF View
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.section.section import Body as PDFBody

class Body(PDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("section.body.pt")

    @property
    def brains(self):
        """ Brains
        """
        return self.context.getFolderContents()[:self.maxbreadth]
