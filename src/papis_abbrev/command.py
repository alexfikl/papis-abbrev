# SPDX-FileCopyrightText: 2024 Alexandru Fikl <alexfikl@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import click

import papis.cli
import papis.config
import papis.document
import papis.logging
import papis.strings

logger = papis.logging.get_logger(__name__)


# {{{ utils


def abbreviate(
    docs: list[papis.document.Document],
    journal_key: str = "journal_abbrev",
) -> list[papis.document.Document]:
    from pyiso4.ltwa import Abbreviate

    abbrev = Abbreviate.create()
    for doc in docs:
        journal = doc.get("journal")
        if not journal:
            logger.warning(
                "Document has no 'journal' key: %s", papis.document.describe(doc)
            )
            continue

        doc[journal_key] = abbrev(journal, remove_part=True)

    return docs


# }}}


# {{{ abbrev


@click.group("abbrev")
@click.help_option("--help", "-h")
def cli() -> None:
    """Manage journal abbreviations according to LTWA"""


# }}}


# {{{ add


@cli.command("add")
@click.help_option("--help", "-h")
@papis.cli.git_option()
@papis.cli.query_argument()
@papis.cli.doc_folder_option()
@papis.cli.all_option()
@papis.cli.sort_option()
@click.option(
    "--journal-key",
    help="Key name used by the abbreviated journal name",
    type=str,
    default="journal_abbrev",
)
def cli_add(
    query: str,
    journal_key: str,
    git: bool,
    doc_folder: tuple[str, ...],
    _all: bool,
    sort_field: str | None,
    sort_reverse: bool,
) -> None:
    """Add journal abbreviations to documents."""

    documents = papis.cli.handle_doc_folder_query_all_sort(
        query,
        doc_folder,  # type: ignore[arg-type,unused-ignore]
        sort_field,
        sort_reverse,
        _all,
    )
    if not documents:
        logger.warning(papis.strings.no_documents_retrieved_message)
        return

    from papis.api import save_doc

    documents = abbreviate(documents, journal_key=journal_key)
    for doc in documents:
        save_doc(doc)


# }}}

# {{{


@cli.command("bibtex")
@click.help_option("--help", "-h")
@click.argument("bibfile", type=click.Path(), required=True)
def cli_bibtex(bibfile: str) -> None:
    """Add journal abbreviations to BibTeX files."""
    from papis.bibtex import bibtex_to_dict

    docs = [papis.document.from_data(d) for d in bibtex_to_dict(bibfile)]
    abbreviate(docs, journal_key="journal")

    from papis.bibtex import exporter

    with open(bibfile, "w", encoding="utf-8") as outf:
        outf.write(exporter(docs))


# }}}
