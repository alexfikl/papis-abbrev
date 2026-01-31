.. image:: https://github.com/alexfikl/papis-abbrev/workflows/CI/badge.svg
    :alt: Build Status
    :target: https://github.com/alexfikl/papis-abbrev/actions?query=branch%3Amain+workflow%3ACI

papis-abbrev
==============

This command uses `pyiso4 <https://github.com/pierre-24/pyiso4>`__ to abbreviate
journal names. The simplest usage is to just abbreviate a given name using

.. code:: sh

   papis abbrev journal 'Journal of Computational Physics'

but you'll likely be faster if you just write a little script using ``pyiso4``
yourself. The main usage though is adding the abbreviated journal names
documents in your Papis library using the usual query syntax. For example using

.. code:: sh

    papis abbrev add --journal-key journal_abbrev --all <QUERY>

When exporting BibTeX, it's best to set the ``bibtex-journal-key = journal_abbrev``
in your Papis configuration file so that it can pick up the abbreviated journal
name.

The command can also read BibTeX files and directly abbreviate the journal names.
This can be done using

.. code:: sh

   papis abbrev bibtex --out main.abbrev.bib main.bib

Note that this will modify your BibTeX files quite heavily: it will remove
comments, change formatting, etc. This is generally fine if you're working with
a BibTeX formatted by Papis to begin with, but may cause friction otherwise.

LICENSE
=======

This package is licensed under the MIT license (see ``LICENSES/MIT.txt``).
