""" PDF View
"""
import logging
import random
from zope.component import queryUtility
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.folder.folder import IATUnifiedFolder
from eea.converter.browser.app.pdfview import Cover as PDFCover
from eea.converter.browser.app.pdfview import BackCover as PDFBackCover
from eea.pdf.interfaces import IPDFTool
from eea.pdf.utils import getApplicationRoot
logger = logging.getLogger('eea.pdf')


class Cover(PDFCover):
    """ Custom PDF cover
    """
    template = ViewPageTemplateFile('cover.pt')

    @property
    def header(self):
        """ Cover header
        """
        doc = getApplicationRoot(self.context)
        return doc.title_or_id()

    @property
    def themes(self):
        """ Get object themes
        """
        themes = queryMultiAdapter((self.context, self.request),
                                   name='themes-object')

        if not themes:
            return
        for theme in themes.items():
            theme = themes.item_to_short_dict(theme)
            image = theme.get('image', None)
            if not image:
                continue
            theme['image'] = image.replace('/image_icon', '/image_preview')
            yield theme

    def truncate(self, text, length=70, orphans=10,
                 suffix=u".", end=u".", cut=False):
        """ Custom truncate (changed defaults from Cover.truncate)
        """
        return super(Cover, self).truncate(text, length, orphans,
                                           suffix, end, cut)

    def get_pdftheme(self):
        """ PDF Theme
        """
        tool = queryUtility(IPDFTool)
        theme = tool.theme(self.context)
        if not theme:
            theme = tool.globalTheme(self.context)

        return theme

    def get_coverimage(self):
        """ if set imagescollection on PDF Theme, return a random image,
            None otherwise
        """
        imgview = queryMultiAdapter(
            (self.context, self.request), name='imgview')

        if imgview and imgview.display():
            obj = imgview('large')
            # 83520 cover should be an object not image string data
            if isinstance(obj, str):
                return getattr(imgview, 'context', None)
            return obj

        theme = self.get_pdftheme()
        if not theme:
            return None

        container = theme.getImagescollection()
        if not container:
            return None

        results = None

        if IATUnifiedFolder.providedBy(container):
            # container is a folder
            cur_path = '/'.join(container.getPhysicalPath())
            path = {'query': cur_path, 'depth': 1}
            results = container.portal_catalog(
                **{'portal_type': 'Image', 'path': path}
            )
        else:
            # is a container
            results = container.queryCatalog(sort_on=None, batch=False)

        if results is None:
            return None

        return random.sample(results, 1)[0].getObject()

    def display_subtitle(self):
        """ Check if cover should be displayed for the current theme
        """
        theme = self.get_pdftheme()
        return getattr(theme, 'coverSubtitle', True)


class BackCover(PDFBackCover):
    """ PDF Back cover
    """
