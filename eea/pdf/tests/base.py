""" Testing
"""
import os
import shutil
import tempfile
from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting

class EEAFixture(PloneSandboxLayer):
    """ EEA Testing Policy
    """
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """ Setup Zope
        """

        self.PATH = tempfile.mkdtemp()
        os.environ["EEADOWNLOADS_PATH"] = self.PATH
        os.environ["EEADOWNLOADS_NAME"] = 'downloads'

        import eea.downloads
        import eea.pdf

        self.loadZCML(package=eea.downloads)
        self.loadZCML(package=eea.pdf)

        z2.installProduct(app, 'eea.downloads')
        z2.installProduct(app, 'eea.pdf')

    def tearDownZope(self, app):
        """ Uninstall Zope
        """
        shutil.rmtree(self.PATH)
        z2.uninstallProduct(app, 'eea.downloads')
        z2.uninstallProduct(app, 'eea.pdf')

    def setUpPloneSite(self, portal):
        """ Setup Plone
        """
        self.applyProfile(portal, 'eea.pdf:default')

        # Login as manager
        setRoles(portal, TEST_USER_ID, ['Manager'])

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")

EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(EEAFIXTURE,),
                                       name='EEAPdf:Functional')
