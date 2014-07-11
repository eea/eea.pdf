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

Dependencies
============

1. `eea.converter`_
2. `wkhtmltopdf`_
3. `pdftk`_

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
