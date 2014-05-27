""" Custom content
"""
from Products.ATContentTypes.content.base import registerATCT
from eea.pdf.content.dummydocument import Dummydocument
from eea.pdf.config import PROJECTNAME

def register():
    """ Register custom content-types
    """
    registerATCT(Dummydocument, PROJECTNAME)
