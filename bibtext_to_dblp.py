# -*- coding: utf-8 -*-
"""Python script to parse a bibtext file to a bibtext file with dblp references and styling.

Example:
    python bibtext_to_dblp <bibtext input file> <output file>
"""

import requests
import os
from typing import Optional
import time


def parse_bibtext_file_titles(file_path: str) -> list[str]:
    """Parse a bibtext file titles, using pybibtext, into a list of titles.

    Args:
        file_path (str): File path of the file to parse.

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
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def get_url(title: str) -> Optional[str]:
    """Search DBLP with a publication title and parse the pdf from the best result.json.

    Args:
        title (str): Title of th ePublicatiuon to search for.

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
        Optional[str]: Bibtext reference for the publication or None if an error occurred.
    """
    r = requests.get(url + ".bib")
    if r.status_code == 200:
        return r.text
    else:
        return None


def bibtext_to_dblp(outpu_file: str, input_file: str):
    """Convert a bibtext file into a bibtext file with dblp styling.

    Args:
        outpu_file (str): Destination for the new file.
        input_file (str): Input file to parse bibtext citations from.
    """
    titles = parse_bibtext_file_titles(input_file)
    errors = []
    dblp_citations = []
    for publication in titles:
        if site_url := get_url(publication):
            if dblp_citation := get_dblp_bibtext(site_url):
                dblp_citations.append(dblp_citation)
            else:
                errors.append(publication)
        else:
            errors.append(publication)

    if dblp_citations:
        with open(outpu_file, "w") as outFile:
            outFile.write("\n".join(dblp_citations))
        print("New bibtext file written to", site_url)
    else:
        print("No citations to write.")
    if errors:
        print("Could not create citations for:")
        print("\n".join(errors))


if __name__ == "__main__":
    input_file = "repro_ecir_track.bib"
    outpu_file = "repro_ecir_track_dblp.bib"
    bibtext_to_dblp(outpu_file, input_file)
