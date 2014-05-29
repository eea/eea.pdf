""" GenericSetup export/import XML adapters
"""
import os
from zope.component import queryMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from eea.pdf.config import PDFFILE
#
# PDF Tool
#
def importPDFTool(context):
    """Import settings."""
    logger = context.getLogger('eea.pdf')

    body = context.readDataFile(PDFFILE)
    if body is None:
        logger.info("Nothing to import")
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_pdf', None)
    if not tool:
        logger.info('portal_pdf tool missing')
        return

    importer = queryMultiAdapter((tool, context), IBody)
    if importer is None:
        logger.warning("Import adapter missing.")
        return

    # set filename on importer so that syntax errors can be reported properly
    subdir = getattr(context, '_profile_path', '')
    importer.filename = os.path.join(subdir, PDFFILE)

    importer.body = body
    logger.info("Imported.")

def exportPDFTool(context):
    """Export settings."""
    logger = context.getLogger('eea.pdf')
    site = context.getSite()
    tool = getToolByName(site, 'portal_pdf')

    if tool is None:
        logger.info("Nothing to export")
        return

    exporter = queryMultiAdapter((tool, context), IBody)
    if exporter is None:
        logger.warning("Export adapter missing.")
        return

    context.writeDataFile('pdf.xml',
                          exporter.body, exporter.mime_type)
    logger.info("Exported.")
