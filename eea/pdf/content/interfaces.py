"""
PDF content interfaces

    >>> portal = layer['portal']

"""
from zope.interface import Interface

class IPDFTool(Interface):
    """
    Local utility to store and customize PDF themes

        >>> from zope.component import queryUtility
        >>> from eea.pdf.interfaces import IPDFTool
        >>> ptool = queryUtility(IPDFTool)
        >>> ptool
        <PDFTool at /plone/portal_pdf>

    """

    def themes():
        """ Available themes

            >>> ptool.themes()
            <generator object themes at ...>

        """


class IPDFTheme(Interface):
    """
    Content-type

        >>> cid = ptool.invokeFactory('PDFTheme', id='zu')
        >>> theme = ptool[cid]
        >>> theme
        <PDFTheme at /plone/portal_pdf/zu>

    """
