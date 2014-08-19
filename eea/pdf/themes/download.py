""" Download PDF
"""
from eea.converter.browser.app.download import Pdf
from eea.pdf.cache import ramcache, cacheKey

class Download(Pdf):
    """ Download PDF
    """
    @ramcache(cacheKey, dependencies=['eea.pdf'])
    def make_pdf(self):
        """ Cached PDF maker
        """
        return super(Download, self).make_pdf()
