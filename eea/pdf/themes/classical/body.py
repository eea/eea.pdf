""" PDF View
"""
import os
import urllib
import urllib2
import urlparse
import contextlib
import logging
from bs4 import BeautifulSoup
from eea.converter.browser.app.pdfview import Body as PDFBody
from eea.converter.utils import absolute_url
logger = logging.getLogger('eea.pdf')

class Body(PDFBody):
    """ Custom PDF body
    """

    def fix_daviz(self, html):
        """ Replace daviz iframes with fallback images
        """
        soup = BeautifulSoup(html)
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src')
            if u'embed-chart' in src:
                src = src.replace('embed-chart', 'embed-chart.svg')
                src = absolute_url(self.context,
                        url=src, default=src, view='embed-chart.svg')
                base = src.split('embed-chart.svg')[0]
                query = urlparse.parse_qs(urlparse.urlparse(src).query)
                chart = query.get('chart')[0]
            elif u'embed-dashboard' in src:
                src = src.replace('embed-dashboard', 'embed-dashboard.svg')
                src = absolute_url(self.context,
                        url=src, default=src, view='embed-dashboard.svg')
                base = src.split('embed-dashboard.svg')[0]
                query = urlparse.parse_qs(urlparse.urlparse(src).query)
                chart = query.get('dashboard')[0]
            else:
                continue

            if not src.startswith('http'):
                src = os.path.join(self.context.absolute_url(), src)
            if not base.startswith('http'):
                base = os.path.join(self.context.absolute_url(), base)

            src = list(urlparse.urlparse(src))
            query = urlparse.parse_qs(src[4])
            query.update({
                'tag:int': 1,
                'safe:int': 0
            })
            src[4] = urllib.urlencode(query, doseq=True)
            src = urlparse.urlunparse(src)

            code = ''
            try:
                with contextlib.closing(
                    urllib2.urlopen(src, timeout=15)) as conn:
                    code = conn.read()
            except Exception, err:
                logger.exception(err)

            if code:
                img = BeautifulSoup(code)
            else:
                chart_url = u'%s#tab-%s' % (base, chart)
                qr_url = (
                    u"http://chart.apis.google.com"
                    "/chart?cht=qr&chld=H|0&chs=%sx%s&chl=%s" % (
                        70, 70, urllib2.quote(chart_url)))
                img = BeautifulSoup(u'''
                <div class="portalMessage warningMessage pdfMissingImage">
                  <img class="qr" src="%(qr_url)s" />
                  <span>
                    This area contains interactive content
                    which is not printable.
                    You may visit the online version at:
                  </span>
                  <a href="%(url)s">%(url)s</a>
                </div>''' % {'url': chart_url, 'qr_url': qr_url})
            iframe.replaceWith(img)
        return soup.find_all('html')[0].decode()

    def fix_portalMessages(self, html):
        """ Remove portal messages
        """
        soup = BeautifulSoup(html)
        for portalMessage in soup.find_all('p', {'class': 'portalMessage'}):
            portalMessage.extract()
        return soup.find_all('html')[0].decode()

    def __call__(self, **kwargs):
        # Cheat condition @@plone_context_state/is_view_template
        self.request['ACTUAL_URL'] = self.context.absolute_url()
        html = super(Body, self).__call__(**kwargs)
        try:
            html = self.fix_portalMessages(html)
            html = self.fix_daviz(html)
        except Exception, err:
            logger.exception(err)
        return html
