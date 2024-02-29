# SPDX-FileCopyrightText: 2023 Alexandru Fikl <alexfikl@gmail.com>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import click

import papis.api
import papis.cli
import papis.config
import papis.document
import papis.logging
import papis.strings

logger = papis.logging.get_logger(__name__)


@click.command("abbrev")
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
def cli(
    query: str,
    journal_key: str,
    git: bool,
    doc_folder: tuple[str, ...],
    _all: bool,
    sort_field: str | None,
    sort_reverse: bool,
) -> None:
    documents = papis.cli.handle_doc_folder_query_all_sort(
        query, doc_folder, sort_field, sort_reverse, _all
    )
    if not documents:
        logger.warning(papis.strings.no_documents_retrieved_message)
        return

    from pyiso4.ltwa import Abbreviate

    abbrev = Abbreviate.create()
    for doc in documents:
        journal = doc.get("journal")
        if not journal:
            logger.warning(
                "Document has no 'journal' key: %s", papis.document.describe(doc)
            )
            continue

        doc[journal_key] = abbrev(journal, remove_part=True)
        papis.api.save_doc(doc)
