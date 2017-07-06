""" PDF Support
"""
from AccessControl import getSecurityManager
from zope.interface import implementer
from zope.component import queryUtility
from zope.security import checkPermission
from Products.Five.browser import BrowserView
from eea.converter.interfaces import ISupport
from eea.pdf.interfaces import IPDFTool, IPDFAware
from plone.memoize.view import memoize

@implementer(ISupport)
class Support(BrowserView):
    """ PDF Support
    """

    @memoize
    def can_download(self):
        """ Can download context as PDF
        """
        if not IPDFAware.providedBy(self.context):
            return False

        if not checkPermission('eea.pdf.download', self.context):
            return False

        # check for Zope2.View permission of context not just permission
        # to download
        if not checkPermission('zope2.View', self.context):
            return False

        tool = queryUtility(IPDFTool)
        if not tool:
            return False

        pdf_theme = tool.theme(self.context)
        if not pdf_theme:
            return False

        return True

    def async(self):
        """ Download PDF asynchronously? True by default
        """
        tool = queryUtility(IPDFTool)
        if not tool:
            return True

        theme = tool.theme(self.context)

        if not theme:
            return True

        return theme.getField('async').getAccessor(theme)()

    def email(self):
        """ User has email
        """
        user = getSecurityManager().getUser()
        getProperty = getattr(user, 'getProperty', lambda name: '')
        return getProperty('email')
