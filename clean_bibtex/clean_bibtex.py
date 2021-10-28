# -*- coding: utf-8 -*-
"""This python script parses an incomplete BibTeX file to a BibTeX file with dblp references and styling.

Example:
    python bibtext_to_dblp <bibtext input file> <output file>
"""

import requests
import click
from typing import Optional
import time


def parse_bibtext_file_titles(file_path: str) -> list[str]:
    """Function to parse the titles of the publications from a BibTeX file.

    Args:
        file_path (str): File path of the BibTeX file to parse.

    Returns:
        list[str]: List with the parsed titles.
    """
    try:
        titles = []
        with open(file_path, "r") as inFile:
            for line in inFile.readlines():
                if line.strip().startswith("title"):
                    title = "".join(line.split("=")[1:])
                    title_clean = title.replace("{", "").replace("}", "").replace(",\n", "").strip()
                    titles.append(title_clean)
        return titles
    except OSError as err:
        print("OS error: {0}".format(err))
        raise
    except ValueError:
        print("Could not parse, bibtext file is malformed.")
        raise
    except BaseException as err:
        print(f"Unexpected {err}, {type(err)}")
        raise


def get_url(title: str) -> Optional[str]:
    """Search DBLP with a publication title and parse the pdf from the best result.json.

    Args:
        title (str): Title of the publication to search for.

    Returns:
        Optional[str]: URL of the DBLP page of the publication or None.
    """
    url = f"https://dblp.org/search/publ/api?q={title}&format=json"
    result = requests.get(url)

    try:
        url = result.json()["result"]["hits"]["hit"][0]["info"]["url"]
        return url
    except:
        return None


def get_dblp_bibtext(url: str) -> Optional[str]:
    """Get the bibtext reference from a dblp publikation site url.

    Args:
        url (str): Url to the publication site.

    Returns:
        Optional[str]: Bibtex reference for the publication or None if an error occurred.
    """
    r = requests.get(url + ".bib")
    if r.status_code == 200:
        return r.text
    else:
        return None


@click.command()
@click.argument("input_file")
@click.argument("outpu_file")
def clean_bibtex(outpu_file: str, input_file: str):
    """Convert an incomplete BibTeX file into a complete BibTeX file with dblp styling.

    Args:
        outpu_file (str): Destination for the new file.
        input_file (str): Input file to parse bibtext citations from.
    """
    titles = parse_bibtext_file_titles(input_file)
    errors = []
    num_publications = str(len(titles))

    click.echo(
        "Requesting citation metadata for {num_publications} publications, this may take a while..."
    )
    with click.progressbar(length=len(titles)) as bar:
        dblp_citations = []
        for publication in titles:
            if site_url := get_url(publication):
                if dblp_citation := get_dblp_bibtext(site_url):
                    dblp_citations.append(dblp_citation)
                else:
                    errors.append(" - " + publication)
            else:
                errors.append(" - " + publication)
            time.sleep(1)  # abide dblp crawl-delay
            bar.update(1)

    if dblp_citations:
        with open(outpu_file, "w") as outFile:
            outFile.write("\n".join(dblp_citations))
        click.echo(f"\nNew BibTeX file written to: {outpu_file}")
    else:
        click.echo("No citations to write.")
    if errors:
        click.echo("\nCould not create citations for:")
        click.echo("\n".join(errors))


if __name__ == "__main__":
    clean_bibtex()
