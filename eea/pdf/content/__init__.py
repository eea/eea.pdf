""" Custom content-types
"""
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types, listTypes
from Products.Archetypes.atapi import registerType
from eea.pdf.content.tool import PDFTool
from eea.pdf.content.theme import PDFTheme
from eea.pdf.config import (
    PROJECTNAME,
    ADD_PERMISSION
)


registerType(PDFTool, PROJECTNAME)
registerType(PDFTheme, PROJECTNAME)

def initialize(context):
    """ Zope 2
    """
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ToolInit(PROJECTNAME + ' Tools',
                tools=[PDFTool],
                icon='content/tool.png'
                ).initialize(context)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=ADD_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
        ).initialize(context)
