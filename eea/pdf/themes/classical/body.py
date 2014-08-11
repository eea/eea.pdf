""" PDF View
"""

import logging
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.converter.browser.app.pdfview import Body as PDFBody
logger = logging.getLogger('eea.pdf')

class Body(PDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile('body.pt')

    def __call__(self, **kwargs):
        # Cheat condition @@plone_context_state/is_view_template
        self.request['ACTUAL_URL'] = self.context.absolute_url()
        self.request.alwaysTranslate = True
        html = super(Body, self).__call__(**kwargs)
        return html
