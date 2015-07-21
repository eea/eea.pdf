""" PDF Support
"""
from AccessControl import getSecurityManager
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

        pdf_theme = tool.theme(self.context)
        if not pdf_theme:
            return False
        body_theme = pdf_theme.body
        # #27539 do not show download pdf if children contain Folder and
        # Collections, they will have the same template which will end
        # up being empty and you will get a master template with empty pages
        if body_theme == "collection.pdf.body":
            context_has_folderish_children = self.context.getFolderContents(
                contentFilter={
                    'portal_type': ['Folder', 'Collection', 'ATTopic']
                })
            return True if not context_has_folderish_children else False

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
