""" Content types
"""
from zope.component import queryUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from eea.pdf.interfaces import IPDFTool

class Themes(object):
    """ Metadata content types
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):

        items = [
            SimpleTerm('-', '-', 'Disable PDF export'),
            SimpleTerm('', '', 'Use portal global settings')
        ]

        tool = queryUtility(IPDFTool)
        items.extend(SimpleTerm(theme.getId(), theme.getId(), theme.Title())
                     for theme in tool.themes())

        return SimpleVocabulary(items)
