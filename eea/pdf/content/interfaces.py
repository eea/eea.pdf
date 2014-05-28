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

    def default():
        """
         Default theme is the first child of type PDFTheme

            >>> print ptool.default()
            None

        """

class IPDFTheme(Interface):
    """
    Content-type

        >>> cid = ptool.invokeFactory('PDFTheme', id='classical')
        >>> theme = ptool[cid]
        >>> theme
        <PDFTheme at /plone/portal_pdf/classical>

        >>> cid = ptool.invokeFactory('PDFTheme', id='modern')
        >>> ptool.default()
        <PDFTheme at /plone/portal_pdf/classical>

    """
