""" Utils
"""
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from plone.app.layout.navigation.interfaces import INavigationRoot

def getApplicationRoot(obj):
    """ Application Root
    """
    portal_url = getToolByName(obj, 'portal_url')
    portal = portal_url.getPortalObject()

    while not INavigationRoot.providedBy(obj) and (
        aq_base(obj) is not aq_base(portal)):
        obj = utils.parent(obj)

    return obj
