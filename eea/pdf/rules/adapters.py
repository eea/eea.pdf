""" Content-rules string substitution
"""
from plone.stringinterp.adapters import BaseSubstitution
from eea.pdf.config import EEAMessageFactory as _

class DownloadTitle(BaseSubstitution):
    """ Download title substitution
    """
    category = _(u'Download')
    description = _(u'Download title')

    def safe_call(self):
        """ Safe call
        """
        return getattr(self.context, 'title_or_id', lambda: '')()

class DownloadEmail(BaseSubstitution):
    """ Download email substitution
    """
    category = _(u'Download')
    description = _(u'Download e-mail')

    def safe_call(self):
        """ Safe call
        """
        return getattr(self.context, 'email', '')

class DownloadUrl(BaseSubstitution):
    """ Download email substitution
    """
    category = _(u'Download')
    description = _(u'Download URL')

    def safe_call(self):
        """ Safe call
        """
        return getattr(self.context, 'fileurl', '')

class DownloadCameFromUrl(BaseSubstitution):
    """ Download email substitution
    """
    category = _(u'Download')
    description = _(u'Download came from URL')

    def safe_call(self):
        """ Safe call
        """
        return getattr(self.context, 'url', '')

class DownloadError(BaseSubstitution):
    """ Download error
    """
    category = _(u'Download')
    description = _(u'Download error')

    def safe_call(self):
        """ Safe call
        """
        return getattr(self.context, 'error', '')
