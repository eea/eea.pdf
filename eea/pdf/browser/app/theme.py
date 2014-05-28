""" Browser views
"""
from Products.Five.browser import BrowserView

class Theme(BrowserView):
    """ Custom view controller
    """
    @property
    def types(self):
        """ Types
        """
        field = self.context.getField('types')
        types = field.getAccessor(self.context)
        return types()
