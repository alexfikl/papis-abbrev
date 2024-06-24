.. image:: https://github.com/alexfikl/papis-abbrev/workflows/CI/badge.svg
    :alt: Build Status
    :target: https://github.com/alexfikl/papis-abbrev/actions?query=branch%3Amain+workflow%3ACI

papis-abbrev
==============

This command uses `pyiso4 <https://github.com/pierre-24/pyiso4>`__ to abbreviate
journal names. The abbreviated journals are added to the document under a new
key. It can be used as

.. code:: sh

    papis abbrev add --journal-key journal_abbrev --all <QUERY>

When using BibTeX, it's best to set the ``bibtex-journal-key = journal_abbrev``
in your Papis configuration file so that it can pick up the abbreviated journal
name.

The command can also read BibTeX files and directly abbreviate the journal names.
This can be done using

.. code:: sh

   papis abbrev bibtex main.bib

LICENSE
=======

This package is licensed under the MIT license (see ``LICENSES/MIT.txt``).
