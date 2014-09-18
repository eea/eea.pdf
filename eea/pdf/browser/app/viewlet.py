""" Custom viewlets
"""
from zope.component import queryMultiAdapter
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Pdf(common.ViewletBase):
    """ Custom viewlet
    """
    render = ViewPageTemplateFile('../zpt/viewlet.pt')

    @property
    def settings(self):
        """ Settings
        """
        if getattr(self, '_settings', None) is None:
            self._settings = queryMultiAdapter(
                (self.context, self.request), name='pdf.support')
        return self._settings

    def async(self):
        """ Async enabled
        """
        return int(self.settings.async())

    def available(self):
        """ Available
        """
        return self.settings.can_download()
