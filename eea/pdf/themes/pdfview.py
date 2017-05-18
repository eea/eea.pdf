""" PDF View
"""
import logging
import tempfile
from zope.component import queryUtility
from eea.converter.config import TMPDIR
from eea.converter.pdf.adapters import OptionsMaker as PDFOptionsMaker
from eea.converter.pdf.adapters import BodyOptionsMaker as PDFBodyOptionsMaker
from eea.converter.pdf.adapters import CoverOptionsMaker as PDFCoverOptionsMaker
from eea.converter.pdf.adapters import \
    BackCoverOptionsMaker as PDFBackCoverOptionsMaker
from eea.converter.pdf.adapters import \
    DisclaimerOptionsMaker as PDFDisclaimerOptionsMaker

from eea.pdf.interfaces import IPDFTool
logger = logging.getLogger('eea.pdf')

class Mixin(object):
    """ Mixin Utility
    """
    @property
    def theme(self):
        """ Get associated theme
        """
        theme = getattr(self, '_theme', '')
        if theme != '':
            return theme

        ptool = queryUtility(IPDFTool)
        if ptool:
            self._theme = ptool.theme(self.context)
        else:
            self._theme = None
        return self._theme

    def getValue(self, name, default=''):
        """ Get theme based options
        """
        theme = self.theme
        if not theme:
            return default

        field = theme.getField(name)
        if not field:
            return default

        accessor = field.getAccessor(theme)
        if not accessor:
            return default

        return accessor()

    def getTemplate(self, name, default=None):
        """ Get template by name
        """
        template = self.getValue(name)
        if not template:
            return default
        return self.context.restrictedTraverse(template, default)

    def staticfy(self, filename, body, suffix='.html'):
        """ Return file path served from a temporary location
        :param filename: Filename
        :type filename: str
        :param body: File content
        :type body: str
        :param suffix: File prefix
        :type suffix: str
        :return: File location
        :rtype: str
        """
        with tempfile.NamedTemporaryFile(
                prefix=filename, suffix=suffix,
                dir=TMPDIR(), delete=False) as ofile:
            ofile.write(body)
            return ofile.name

    def set_template(self, name, static=False, suffix='.html'):
        """ Set Templates
        :param name: Template name to retrieve
        :type name: str
        :param static: Boolean indicating whether the template url is static
        :type static: bool
        :param suffix: Template suffix
        :type suffix: str
        :return: path to template, either locally from tmp or from site location
        :rtype: str
        """
        _name = "_" + name
        parent_attribute = getattr(self, _name, None)
        if not self.theme:
            setattr(self, _name, '')
            return getattr(self, _name)

        if parent_attribute is None:
            template = self.getValue(name)
            if not getattr(self.theme, 'staticFooterAndHeader', False) \
                    and not static:
                setattr(self, _name, ('/'.join((self.context.absolute_url(),
                                                template)) if template else ''))
            else:
                try:
                    body = self.getTemplate(name)
                    if not body:
                        setattr(self, _name, '')
                        return ''
                    body = body()
                    if isinstance(body, unicode):
                        body = body.encode('utf-8')
                except Exception:
                    setattr(self, _name, '')
                else:
                    setattr(self, _name, self.staticfy(template or name, body,
                                                       suffix=suffix))
        return getattr(self, _name)


class OptionsMaker(PDFOptionsMaker, Mixin):
    """ Global options maker
    """
    def __init__(self, context):
        super(OptionsMaker, self).__init__(context)
        self._options = None
        self._timeout = None

    @property
    def timeout(self):
        """ Get timout from theme
        """
        if not self.theme:
            return super(OptionsMaker, self).timeout

        if self._timeout is None:
            self._timeout = self.getValue('timeout', 10)
        return self._timeout

    @property
    def options(self):
        """ Get global options
        """
        if self._options is not None:
            return self._options

        options = super(OptionsMaker, self).options
        if not self.theme:
            return options

        offset = self.getValue('offset')
        index = 0
        for idx, option in enumerate(options):
            if option == '--page-offset':
                index = idx + 1
                break

        if index:
            options[index] = repr(offset)
        else:
            options.extend(
                ['--page-offset', repr(offset)]
            )

        javascript = self.getValue('javascript', True)
        if not javascript:
            options.append('--disable-javascript')

        # Wait for javascript in milliseconds (200 ms is default)
        delay = self.getValue('javascriptdelay', 0.2)
        delay = max(0.2, delay)
        timeout = self.timeout or 9999
        if 0.2 < delay < timeout:
            delay *= 1000
            options.extend(['--javascript-delay', repr(delay)])

        self._options = options
        return self._options

class BodyOptionsMaker(PDFBodyOptionsMaker, Mixin):
    """ Custom PDF options maker
    """

    def __init__(self, context):
        super(BodyOptionsMaker, self).__init__(context)
        self._body = None
        self._header = None
        self._footer = None
        self._toc = None
        self._toc_links = None


    @property
    def body(self):
        """ Safely get pdf.body
        """
        if not self.theme:
            self._body = ''

        if self._body is None:
            template = self.getValue('body')
            self._body = ('/'.join((self.context.absolute_url(), template))
                          if template else '')
        return self._body


    @property
    def header(self):
        """ Safely get pdf.header
        """
        return self.set_template('header')

    @property
    def footer(self):
        """ Safely get pdf.footer
        """
        return self.set_template('footer')

    @property
    def toc(self):
        """ Table of contents
        """
        template = self.getValue('toc')
        # wkhtmltopdf doesn't support URLs for TOC xsl
        # To be un-commented when fixed by wkhtmltopdf.
        # self._toc = ('/'.join((self.context.absolute_url(), template))
        #                 if template else '')

        # 24351; disable toc if tocdepth attribute is found and is == 0
        if not template or getattr(self.context, 'tocdepth', -1) == 0:
            self._toc = ''
            return self._toc
        return self.set_template("toc", static=True, suffix='.xsl')

    @property
    def toc_links(self):
        """ Enable/Disable Table of contents links
        """
        if not self.theme:
            self._toc_links = False

        if self._toc_links is None:
            self._toc_links = self.getValue('toclinks', None)
        return self._toc_links


class CoverOptionsMaker(PDFCoverOptionsMaker, Mixin):
    """ Custom cover options maker
    """
    def __init__(self, context):
        super(CoverOptionsMaker, self).__init__(context)
        self._body = None

    @property
    def body(self):
        """ Safely get pdf.cover
        """
        if not self.theme:
            self._body = ''

        if self._body is None:
            template = self.getValue('cover')
            self._body = ('/'.join((self.context.absolute_url(), template))
                          if template else '')
        return self._body

class BackCoverOptionsMaker(PDFBackCoverOptionsMaker, Mixin):
    """ Custom back.cover options maker
    """
    def __init__(self, context):
        super(BackCoverOptionsMaker, self).__init__(context)
        self._body = None

    @property
    def body(self):
        """ Safely get pdf.cover.back
        """
        if not self.theme:
            self._body = ''

        if self._body is None:
            template = self.getValue('backcover')
            self._body = ('/'.join((self.context.absolute_url(), template))
                          if template else '')
        return self._body

class DisclaimerOptionsMaker(PDFDisclaimerOptionsMaker, Mixin):
    """ Custom pdf.disclaimer
    """
    def __init__(self, context):
        super(DisclaimerOptionsMaker, self).__init__(context)
        self._body = None

    @property
    def body(self):
        """ Safely get disclaimer
        """
        if not self.theme:
            self._body = ''

        if self._body is None:
            template = self.getValue('disclaimer')
            self._body = ('/'.join((self.context.absolute_url(), template))
                          if template else '')
        return self._body
