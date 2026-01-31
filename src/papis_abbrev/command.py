# SPDX-FileCopyrightText: 2024 Alexandru Fikl <alexfikl@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

import click

import papis.cli
import papis.logging

if TYPE_CHECKING:
    from papis.document import Document

    DocumentT = TypeVar("DocumentT", Document, dict[str, Any])

logger = papis.logging.get_logger(__name__)


# {{{ utils


def abbreviate(
    docs: list[DocumentT],
    journal_key: str = "journal_abbrev",
) -> list[DocumentT]:
    from pyiso4.ltwa import Abbreviate

    abbrev = Abbreviate.create()

    from papis.document import describe

    for doc in docs:
        journal = doc.get("journal")
        if not journal:
            logger.warning("Document has no 'journal' key: %s", describe(doc))
            continue

        doc[journal_key] = abbrev(journal.replace("\\", ""), remove_part=True)

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
    all_: bool,
    sort_field: str | None,
    sort_reverse: bool,
) -> None:
    """Add journal abbreviations to documents"""

    documents = papis.cli.handle_doc_folder_query_all_sort(
        query,
        doc_folder,
        sort_field,
        sort_reverse,
        all_,
    )
    if not documents:
        from papis.strings import no_documents_retrieved_message

        logger.warning(no_documents_retrieved_message)
        return

    from papis.api import save_doc

    documents = abbreviate(documents, journal_key=journal_key)
    for doc in documents:
        save_doc(doc)


# }}}

# {{{ bibtex


@cli.command("bibtex")
@click.help_option("--help", "-h")
@click.argument("bibfile", type=click.Path(), required=True)
@click.option(
    "-o",
    "--outfile",
    default=None,
    type=click.Path(),
    help="Output file for the BibTeX entries with abbreviated journal names.",
)
def cli_bibtex(bibfile: str, outfile: str | None) -> None:
    """Add journal abbreviations to BibTeX files"""
    from papis.bibtex import bibtex_to_dict
    from papis.document import from_data

    docs = [from_data(d) for d in bibtex_to_dict(bibfile)]
    abbreviate(docs, journal_key="journal")

    from papis.bibtex import to_bibtex

    if outfile is None:
        click.echo("\n\n".join(to_bibtex(doc) for doc in docs))
    else:
        logger.info("Writing abbreviated BibTeX file: '%s'.", outfile)

        with open(outfile, "w", encoding="utf-8") as outf:
            outf.write("\n\n".join(to_bibtex(doc) for doc in docs))


# }}}

# {{{ journal


@cli.command("journal")
@click.help_option("--help", "-h")
@click.argument("journal", nargs=-1, required=True)
def cli_journal(journal: list[str]) -> None:
    """Abbreviate a single journal name"""
    from pyiso4.ltwa import Abbreviate

    abbrev = Abbreviate.create()
    click.echo(abbrev(" ".join(journal).title().replace("\\", ""), remove_part=True))


# }}}
