=======
EEA PDF
=======
.. image:: http://ci.eionet.europa.eu/job/eea.pdf-www/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.pdf-www/lastBuild
.. image:: http://ci.eionet.europa.eu/job/eea.pdf-plone4/badge/icon
  :target: http://ci.eionet.europa.eu/job/eea.pdf-plone4/lastBuild

This package allows your users to download Plone content as PDF files. As admin
you can define specific PDF themes per content-type.

.. note ::

  Requires `wkhtmltopdf`_ and `pdftk`_ system-packages installed on your server.
  See `eea.converter`_ documentation for more details.

Contents
========

.. contents::

Main features
=============

1. Adds download as PDF action at the bottom of the page
2. Possibility to define custom PDF themes per content-type

Install
=======

- Add eea.pdf to your eggs section in your buildout and re-run buildout.
  You can download a sample buildout from
  https://github.com/eea/eea.pdf/tree/master/buildouts/plone4
- Install eea.pdf within Site Setup > Add-ons

Getting started
===============

1. Go to Site Setup > PDF Settings
2. Customize an existing PDF theme or add a new one
3. Go to Home page and click on download as pdf icon at the bottom of the page
   or directly access http://localhost:8080/Plone/front-page/download.pdf

PDF Theme options
=================
For more information about wkhtmltopdf options like Table of contents XSL file,
header and footer parameters, etc. see `wkhtmltopdf`_ documentation.

Cover
-----
A page template to be used for PDF Cover. Leave empty to disable it.
Default: pdf.body

Disclaimer
----------
A page template containing copyright and author information. This page will be
placed between cover and PDF body. Leave empty to skip it.
Default: pdf.disclaimer

Body
----
A page template to be used for PDF body. An empty value will skip PDF body.
Default: pdf.body

Back Cover
----------
A page template to be used for back cover. Leave empty to disable back cover.
Default: pdf.cover.back

Header
------
A page template to be used as PDF body header. This will not appear on cover,
disclaimer or back cover. Leave empty for no header.
Default: pdf.header

Footer
------
A page template to be used as PDF body footer. This will not appear on cover,
disclaimer or back.cover. Leave empty for no footer.
Default: pdf.footer

Table of contents
-----------------
An XSL page template to be used for PDF Table of contents. See `wkhtmltopdf`_
documentation for more information about XSL format. Leave empty to disable
Table of contents.
Default: pdf.toc

Table of contents links
-----------------------
Enable or disable Table of Contents internal links and also
PDF bookmarks (outline)
Default: False

JavaScript
----------
Enable or disable javascript.
Default: True


Timeout
-------
Abort PDF conversion after this number of seconds
Default: 60

Offset
------
Start counting pages within PDF Body from this number. Usefull when cover and/or
disclaimer are enabled.
Default: 0

Maximum depth
-------------
This option defines the maximum depth a folderish item can go while recursively
includes it's children within PDF.
Default: 1 (include only direct children, non-folderish ones)

Maximum breadth
---------------
This options limit the number of direct children a folderish item can include
within PDF.
Default: 100

Maximum items
-------------
The total items to be included within PDF export for a folderish item, including
depth and breadth.
Default: 1000

Portal types
------------
Apply this theme to selected portal types.
Default:


Custom permissions
==================
Custom permissions added by this package

Can download PDF (eea.pdf.download)
-----------------------------------
Assign this permission to roles that you want to be able to download content as PDF
Default: Owner, Manager, Editor

Can customize PDF (eea.pdf.customize)
-------------------------------------
Assign this permission to roles that you want to be able to contextually customize
the output PDF look and feel
Default: Manager, Site Administrator

Dependencies
============

1. `eea.converter`_
2. `wkhtmltopdf`_
3. `pdftk`_
4. `eea.cache`_ (optional)

Source code
===========

- Latest source code (Plone 4 compatible):
  https://github.com/eea/eea.pdf


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA PDF (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

More details under docs/License.txt


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: http://www.eea.europa.eu/
.. _eea.converter: http://eea.github.com/docs/eea.converter
.. _wkhtmltopdf: http://wkhtmltopdf.org
.. _pdftk: http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/
.. _eea.cache: http://eea.github.com/docs/eea.cache
