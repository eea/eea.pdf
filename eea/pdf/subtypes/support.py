""" PDF Support
"""
from zope.interface import implementer
from zope.component import queryUtility
from zope.security import checkPermission
from Products.Five.browser import BrowserView
from eea.converter.interfaces import ISupport
from eea.pdf.interfaces import IPDFTool, IPDFAware

@implementer(ISupport)
class Support(BrowserView):
    """ PDF Support
    """
    @property
    def can_download(self):
        """ Can download context as PDF
        """
        if not IPDFAware.providedBy(self.context):
            return False

        if not checkPermission('eea.pdf.download', self.context):
            return False

        tool = queryUtility(IPDFTool)
        if not tool:
            return False

        if not tool.theme(self.context):
            return False

        return True
