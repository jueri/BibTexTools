from __future__ import annotations
import json
import warnings
from dataclasses import dataclass, field
from typing import Dict, List, Union, Any

STANDARD_FIELDS = [
    "address",
    "author",
    "booktitle",
    "chapter",
    "crossref",
    "edition",
    "editor",
    "howpublished",
    "institution",
    "journal",
    "month",
    "note",
    "number",
    "organization",
    "pages",
    "publisher",
    "school",
    "series",
    "title",
    "volume",
    "year",
    "type",
    "key",
]


def extract_content_of_field(field_value: str) -> str:
    """Extract the value of a field by stripping all trailing whitespaces and "{}".

    Args:
        field_value (str): Input field string to be cleaned.

    Returns:
        str: Value of the field.
    """
    assert isinstance(field_value, str)
    field_value = field_value.strip()
    return field_value.replace("{", "").replace("}", "")


class Field:
    """BibTex field object containing a field name and a field value."""

    def __init__(self, name, value):
        self.name: str = name
        self.value: str = value

    def to_bibtex(self) -> str:
        """Serialize the field object into a BibTex string.

        Returns:
            str: Bibtex string of the field.
        """
        return self.name + " = " + self.value

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:
        """Serielize the field object into a dictionary.

        Returns:
            str: Dictionary of the field.
        """
        value = extract_content_of_field(self.value)
        return {self.name: int(value) if value.isdigit() else value}


class Author:
    """Author name object."""

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.mid = [str]

    def abbreviate(self, middle: bool) -> Author:
        """Abbreviate the author name, with or without middle names.

        Args:
            middle (bool): True if the middle names should also be abbreviated.

        Returns:
            str: Full abbreviated name string.
        """

        def _abbreviate_name(name: str) -> str:
            """Abbreviate a name if not already abbreviated.

            Args:
                name (str): Name to be abbreviated.

            Returns:
                str: Abbreviated name.
            """
            if name.endswith("."):
                if " " in name:  # First III.
                    name_split = name.split(" ")
                    assert len(name_split) == 2
                    return name_split[0][0].upper() + "." + " " + name_split[1]
                else:  # Name is allready abbreviated
                    return name
            else:
                return name[0].upper() + "."

        if " Jr." in self.last:
            last = self.last.split(" ")[0]
        else:
            last = self.last

        self.first_short = _abbreviate_name(self.first)
        name_short = last + ", " + _abbreviate_name(self.first)

        if middle:
            mid_short = []
            for name in self.mid:
                mid_short.append(_abbreviate_name(name))
                name_short += " " + _abbreviate_name(name)
            self.mid_short = mid_short

        if " Jr." in self.last:
            name_short += " Jr."

        self.name_short = name_short
        return self


class Author_field(Field):
    """Dedicated field for the author information."""

    def __init__(self, name, value):
        super().__init__(name, value)
        self.author_list = self.split_authorlist()

    def split_authorlist(self) -> List[Author]:
        """Create a list of author objects from the value of the field.

        Returns:
            List[Author]: List of author objects.
        """
        author_list = []
        authors_str = extract_content_of_field(self.value)

        for author in authors_str.split(" and "):
            if "," in author:
                author_parts = author.split(", ")

                last = author_parts[0]
                mid = author_parts[1:-1]
                first = author_parts[-1]
            else:
                author_parts = author.split(
                    " "
                )  # if author name is not comma seperated names are in order
                first = author_parts[0]
                mid = []
                last = author_parts[-1]
                for name in author_parts[1:-1]:
                    if name.lower() == "von":
                        last = name + " " + last
                    else:
                        mid.append(name)

            author_obj = Author(first, last)
            author_obj.mid = mid
            author_list.append(author_obj)

        return author_list

    def abbreviate(self, middle: bool) -> Author_field:
        """Abbreviate all authors from the author list.

        Args:
            middle (bool): True if middle names should be included.

        Returns:
            List[str]: List of abbreviated author names.
        """
        author_list_abbreviated = []
        for author in self.author_list:
            author_list_abbreviated.append(author.abbreviate(middle))

        self.author_list_abbreviated = author_list_abbreviated
        return self

    def to_bibtex(self) -> str:
        """Serielize into a BibTex string.

        Returns:
            str: Field as BibTex string.
        """
        return self.name + " = " + self.value.replace(" and ", " and\n")


class Journal_field(Field):
    """Dedicated field for journal information."""

    def __init__(self, name, value):
        super().__init__(name, value)

    # def abbreviate(TODO):


@dataclass
class Entry:
    """Entry class representing a document in a BibTex bibliography."""

    string: str = ""
    fields: List[str] = field(default_factory=list)

    def add_field(self, field_name: str, value: str):
        """Add a field to the entry to store information about the document. The field is added
        according to the field type to store the information correctly.

        Args:
            field_name (str): Field type.
            value (str): Value of the field.
        """
        if field_name not in STANDARD_FIELDS:
            warnings.warn(
                UserWarning(f'Warning: "{field_name}" is not a standard Bibtex field')
            )
        if field_name == "author":
            field = Author_field(field_name, value)
            setattr(self, field_name, field)
        elif field_name == "journal":
            field = Journal_field(field_name, value)  # type: ignore
            setattr(self, field_name, field)
        else:
            field = Field(field_name, value)  # type: ignore
            setattr(self, field_name, field)
        self.fields.append(field_name)

    def to_bibtex(self, fields: List[str] = []) -> str:
        """Serialize the full Entry object into a BibTex string.

        Returns:
            str: Bibtex string of the Entry.
        """
        bibtex = []
        assert len(self.fields) > 1
        if fields == []:
            fields = self.fields
        for field in fields:
            if field in ["key", "type"]:
                continue
            bibtex.append(self.__getattribute__(field).to_bibtex())

        return ",\n".join(
            ["@" + self.type.value + "{" + self.key.value] + bibtex + ["}"]  # type: ignore
        )

    def to_dict(self, fields: List[str] = []) -> Dict[str, Dict[str, Union[str, int]]]:
        """Serielize the entry object into a dictionary.

        Returns:
            str: Dictionary of all fields.
        """
        assert len(self.fields) > 1
        bibtex: Dict[str, Any] = {}
        if fields == []:
            fields = self.fields

        for field in set(fields):
            if field == "key":
                continue
            bibtex = {**bibtex, **self.__getattribute__(field).to_dict()}  # join dicts
        return {self.key.value: bibtex}  # type: ignore

    def abbreviate_names(self, middle: bool) -> Entry:
        """Abbreviate all author names from entry. The full names are preserved as `authors_full`.

        Args:
            middle (bool): Abbriviate or delete the moddle names.

        Returns:
            Entry: The full entry with the abbreviated and full names.
        """
        assert "author" in self.fields
        author_full = self.author  # type: ignore
        self.author = self.author.abbreviate(middle=middle)  # type:ignore
        self.author_full = author_full
        return self

    # def abbreviate_journals()
    #   TODO


@dataclass
class Bibliography:
    """Bibliography object representing the full BibTex bibliography."""

    entries: List[Entry] = field(default_factory=list)

    def to_bibtex(self, fields: List[str] = []) -> str:
        """Serialize the bibliography object into a BibTex string.

        Returns:
            str: Bibtex string of the Bibliography.
        """
        assert len(self.entries) > 1
        bibtex = []
        for entry in self.entries:
            bibtex.append(entry.to_bibtex(fields))
        return "\n\n\n".join(bibtex)

    def to_bib(self, path: str, fields: List[str] = []):
        """Write the bibliography into a .bib file.

        Args:
            path (str): Path to the bib file to write to.
        """
        with open(path, "w") as fout:
            fout.write(self.to_bibtex(fields))

    def to_json(self, path: str, fields: List[str] = []):
        """Write the bibliography into a JSON file.

        Args:
            path (str): Path to the JSON file.
        """
        bibtex: Dict[str, Any] = {}
        assert len(self.entries) > 1
        for entry in self.entries:
            bibtex = {**bibtex, **entry.to_dict(fields)}

        with open(path, "w") as fout:
            json.dump(bibtex, fout, indent=4)

    def abbreviate_names(self, middle: bool) -> Bibliography:
        """Abbreviate all author names from all entries.

        Args:
            middle (bool): Abbreviate the middle name.

        Returns:
            Bibliography: The full bibliography with abbreviated names.
        """
        abbreviated_entries = []
        for entry in self.entries:
            if "author" in entry.fields:
                abbreviated_entries.append(entry.abbreviate_names(middle))
            else:
                abbreviated_entries.append(entry)
        self.entries = abbreviated_entries
        return self

    # def abbreviate_journals(
    # TODO)
