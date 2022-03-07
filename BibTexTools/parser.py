import re
from typing import Tuple

from BibTexTools.bibliography import Bibliography, Entry

TRAILING_WHITESPACES = re.compile(r"\s\s+")


def clean_line(line: str) -> str:
    """Remove trailing white spaces and newlines from string.

    Args:
        line (str): String to be cleaned.

    Returns:
        str: Cleaned string.
    """
    line = line.replace("\n", "")  # clean newline
    line = TRAILING_WHITESPACES.sub("", line)

    return line.strip()


def get_type(line: str) -> str:
    """Extract the value of a BibTex type field following the "@" at the beginning of a BibTex reference.

    Args:
        line (str): Full line the type string is expected in.

    Returns:
        str: Document type.
    """
    results = re.match(r"@(.*){", line)
    if results:
        entry_type = results.groups()[0]
        return entry_type


def get_key(line: str) -> str:
    """Extract the citation key of a BibTex Document.

    Args:
        line (str): Full line the key string is expected in.

    Returns:
        str: Document citation key.
    """
    results = re.match(r"@.*{(.*),", line)
    if results:
        key = results.groups()[0]
        return key


def parse_field(line: str) -> Tuple[str, str]:
    """Parse a BibTex field into its field name and field value.

    Args:
        line (str): Full line containing the field and value.

    Returns:
        Tuple[str, str]: Name of the BibTex field and its value.
    """
    assert "=" in line
    field_str = line.split("=")
    field_name: str = field_str[0].strip()
    value: str = field_str[-1]
    value = value.strip(" ,")
    return field_name, value


class Parser:
    """Load a BibTex bibliography."""

    def parse(self, bibtex_string: str) -> Bibliography:
        """Parse a BibTex string into a BibTexTools bibliography.

        Args:
            bibtex_string (str): Multiline string containing one or more BibTex entries to be parsed.

        Returns:
            Bibliography: Bibliography object.
        """
        bibliography = Bibliography()
        entry = Entry()
        field_str: str = ""

        for line in bibtex_string.split("\n"):
            line = clean_line(line)
            if line == "}":
                continue
            elif not line.strip():
                continue
            field_str += line + " "

            if field_str.startswith("@"):  # entry start
                if hasattr(entry, "key"):
                    bibliography.entries.append(entry)  # add last entry
                    entry = Entry()

                entry.string += field_str
                entry.add_field("type", get_type(field_str))
                entry.add_field("key", get_key(field_str))
                field_str = ""

            elif field_str.count("{") != field_str.count("}"):  # incomplete field
                continue
            else:
                field_name, value = parse_field(field_str)
                entry.add_field(field_name, value)
                entry.string += field_str
                field_str = ""

        bibliography.entries.append(entry)
        return bibliography

    def from_file(self, bibtes_path: str) -> Bibliography:
        """Parse a BibTex file into a BibTexTools bibliography.

        Args:
            bibtes_path (str): Path to the bibtex file.

        Returns:
            Bibliography: Bibliography object.
        """
        with open(bibtes_path, "r") as fin:
            bibtex_string = fin.read()

        return self.parse(bibtex_string)
