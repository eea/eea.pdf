=======
EEA PDF
=======
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.pdf/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.pdf/job/develop/display/redirect
  :alt: develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.pdf/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.pdf/job/master/display/redirect
  :alt: master

This package allows your users to download Plone content as PDF files. As admin
you can define specific PDF themes per content-type.

.. note ::

  Requires `wkhtmltopdf`_ system-package installed on your server.
  See `eea.converter`_ documentation for more details.


Contents
========

.. contents::


Main features
=============

1. Adds download as PDF action at the bottom of the page
2. Possibility to define custom PDF themes per content-type
3. Asynchronously generate PDF files and notify users by email when PDF is ready
4. Possibility to temporarily disable dynamic PDF creation by adding an item
   called 'action-download-pdf' within context


Install
=======

- Add eea.pdf to your **eggs** and **zcml** section in your buildout
  and re-run buildout.
  You can download a sample buildout from
  https://github.com/eea/eea.pdf/tree/master/buildouts/plone4
- Install eea.pdf within Site Setup > Add-ons

::

    [instance]
    eggs =
        ...
        eea.pdf

    zcml =
        ...
        eea.pdf


External PDF generator tools
----------------------------
Ensure that you have installed `wkhtmltopdf`_ on your machine. You
can also install `wkhtmltopdf`_ from buildout::

    [buildout]

    parts +=
        wkhtmltopdf

    [wkhtmltopdf]
    recipe = hexagonit.recipe.download
    url = http://eggrepo.apps.eea.europa.eu/pypi/wkhtmltopdf/wkhtmltopdf-0.12.1.tgz

    [instance]
    environment-vars +=
        WKHTMLTOPDF_PATH ${wkhtmltopdf:location}/wkhtmltopdf

Asynchronous setup
------------------
By default all PDFs are generated asynchronous, therefore some extra config is
needed within your buildout in order for this to work properly.

First of all you'll need a folder were to store generated PDF files. For this
you can create it manually within buildout:directory/var/ or you can let buildout
handle it::

    [buildout]

    parts +=
        media-downloads
        media-downloads-temp


    media-downloads-path = ${buildout:directory}/var/downloads/pdf
    media-downloads-temp = ${buildout:directory}/var/downloads/tmp

    [media-downloads]
    recipe = ore.recipe.fs:mkdir
    path = ${buildout:media-downloads-path}
    mode = 0700
    createpath = true

    [media-downloads-temp]
    recipe = ore.recipe.fs:mkdir
    path = ${buildout:media-downloads-temp}
    mode = 0700
    createpath = true

This will create a folder named **downloads** within buildout:directory/var/

Next, in order for this folder to be visible from your website and your users to
be able to download generated PDFs you'll need to tell to your zope instances
about it::

    [buildout]

    media-downloads-name = downloads
    media-downloads-path = ${buildout:directory}/var/downloads/pdf
    media-downloads-temp = ${buildout:directory}/var/downloads/tmp

    [instance]

    environment-vars +=
        EEADOWNLOADS_NAME ${buildout:media-downloads-name}
        EEADOWNLOADS_PATH ${buildout:media-downloads-path}
        EEACONVERTER_TEMP ${buildout:media-downloads-temp}

Also, don't forget to setup `plone.app.async`_

::

    [buildout]

    [instance]
    eggs +=
        plone.app.async
    zcml +=
        plone.app.async-single_db_worker

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
Default: pdf.cover

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

JavaScript Delay
----------------
Wait some seconds for javascript to finish
Default: 0

Timeout
-------
Abort PDF conversion after this number of seconds
Default: 3600

Asynchronous
------------
Generate PDF asynchronously and send an email to the user when it's done
Default: True

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

Content rules
=============
This package uses Plone Content-rules to notify users by email when an asynchronous
PDF job is done. Thus 3 custom content-rules will be added within
Plone > Site Setup > Content-rules

.. warning ::

  As these content-rules are triggered by an asynchronous job, while
  you customize the email template for these content-rules,
  please **DO NOT USE OTHER** string substitutions **that the ones** that start
  with **$download_** as you'll break the download chain.
  Also if you disable these content-rules the users will never know when the
  PDF is ready and what is the link where they can download the output PDF.

Export succeeded
----------------
Notify the person who requested a PDF export that the PDF successfully exported
and provide a link to the downloadable PDF

Export failed
-------------
Notify the person who requested a PDF export that the PDF export failed.

Export failed (admin)
---------------------
Notify admin that there were issues while exporting PDF


Content rules email string substitution
=======================================
In order to be able to easily customize emails sent by this package the following
custom email template string substitutions can be made


${download_came_from_url}
-------------------------
The absolute URL of the Plone object which is downloaded as PDF

${download_email}
-----------------
Email address of the user that triggered the download as PDF action

${download_error}
-----------------
Error traceback when download as PDF job fails

${download_from_email}
----------------------
Site Admin email address customizable via Plone > Site Setup > Mail

${download_from_name}
---------------------
Site Admin name customizable via Plone > Site Setup > Mail

${download_title}
-----------------
Title of the Plone object which is downloaded as PDF

${download_url}
---------------
The absolute URL where the generated output PDF can be downloaded

${download_type}
----------------
Download type. Default to PDF for this package. It is package specific and it
can be PDF, EPUB, etc.


Disable PDF export
==================
You have the possibility to temporarily disable dynamic PDF export contextually
by adding a static PDF file (or a Python Script, Page Template, etc)
within context called **action-download-pdf**. This way /download.pdf will
return this file instead of generating one based on context data.

.. note::

  This works only with folderish items.

Troubleshooting
===============
PDFs are generated asynchronously using a parallel zc.async queue.quota.
The number of workers that will generate PDFs in parallel is automatically
calculated based on the number of zeo-clients registered with
**plone.app.async-*_db_worker**.

As every **db_worker** can handle simultaneously **maximum 3 jobs** (hard-coded in zc.async Agent),
if you have **2 workers** then the maximum number of PDFs that will be generated
at the same time will be **6** (2 workers * 3). Same if you have **5**, you'll get
**15 PDFs** generated at the same time.

If for any reason you don't want them to be generated simultaneously you can set
environment variable **EEAPDF_ASYNC_THREADS** to **1** within buildout::

    [buildout]

    ...

    [instance]

    ...

    environment-vars +=
        EEAPDF_ASYNC_THREADS 1


Also, if you experience issues by having too many simultaneously PDF jobs, you
can limit them in the same way as above.


Dependencies
============

1. `eea.converter`_
2. `eea.downloads`_
3. `wkhtmltopdf`_
4. `plone.app.async`_
5. `eea.cache`_ (optional)

Source code
===========

- Latest source code (Plone 4 compatible):
  https://github.com/collective/eea.pdf


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

.. _EEA: https://www.eea.europa.eu/
.. _eea.converter: https://eea.github.io/docs/eea.converter
.. _eea.downloads: https://eea.github.io/docs/eea.downloads
.. _wkhtmltopdf: http://wkhtmltopdf.org
.. _eea.cache: https://eea.github.io/docs/eea.cache
.. _plone.app.async: https://github.com/plone/plone.app.async#ploneappasync
