import logging
import time
from typing import Optional

import requests

from BibTexTools.bibliography import Bibliography
from BibTexTools.parser import Parser


class Cleaner:
    """Clean a bibliography by searchin the title in the DBLP."""

    def __init__(self, keep_keys: bool = False, keep_unknown: bool = False):
        self.keep_keys = keep_keys
        self.keep_unknown = keep_unknown

    def _search_publication(self, title: str) -> Optional[str]:
        """Search the DBLP with title and retrieve the publication URL of the best match.

        Args:
            title (str): The title of the publication.

        Returns:
            str: URL of the publication site at DBLP or None if an error occured.
        """
        url = f"https://dblp.org/search/publ/api?q={title}&format=json"
        result = requests.get(url)

        if result.status_code != 200:
            logging.info(
                f'Info: Publication with the title "{title}" could not be found.'
            )
            return None

        if result.json()["result"]["hits"].get("hit"):
            return result.json()["result"]["hits"]["hit"][0]["info"]["url"]
        else:
            logging.info(
                f'Info: Publication with the title "{title}" could not be found.'
            )
            return None

    def _get_dblp_bibtext(self, url: str) -> Optional[str]:
        """Get the bibtext reference from a dblp publikation site URL.
        Args:
            url (str): URL to the publication site.
        Returns:
            Optional[str]: Bibtex reference for the publication or None if an error occurred.
        """
        r = requests.get(url + ".bib")
        if r.status_code == 200:
            return r.text
        else:
            logging.error(f'Error: Could not retrieve citation frum URL:"{url}".')
            return None

    def clean(self, bibliography: Bibliography) -> Bibliography:
        """Clean a given bibliography with by searching the title in the DBLP and retrieving the citation from th ebest match.

        Args:
            bibliography (Bibliography): Bibliography to be cleaned.

        Returns:
            Bibliography: Cleaned bibliography.
        """
        cleaned_bib = Bibliography()
        parser = Parser()
        assert len(bibliography.entries) > 0

        for entry in bibliography.entries:
            if publication_url := self._search_publication(entry.title.value):  # type: ignore
                if dblp_citation := self._get_dblp_bibtext(publication_url):
                    cleaned_entry = parser.parse(dblp_citation)
                    cleaned_entry = cleaned_entry.entries[0]  # type: ignore
                    if self.keep_keys:
                        cleaned_entry.key.value = entry.key.value  # type: ignore
                    cleaned_bib.entries.append(cleaned_entry)  # type: ignore
                elif self.keep_unknown:
                    cleaned_bib.entries.append(entry)
            elif self.keep_unknown:
                cleaned_bib.entries.append(entry)

            time.sleep(1)  # abide dblp crawl-delay
        return cleaned_bib
