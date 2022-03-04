import os
from BibTexTools.parser import Parser
from BibTexTools.bibliography import (
    Author_field,
    Entry,
    Author_field,
    Journal_field,
    Author,
)
import pytest

A_string = """@Atype{Akey,
author    = {A1_First von A1_Last and
            von A2_Last, A2_First},
title     = {A_Title},
journal   = {A_Journal},
volume    = {A_Volume},
year      = {A_Year},
url       = {A_Url},
}"""

A_string_fields = """@Atype{Akey,
author    = {A1_First von A1_Last and
            von A2_Last, A2_First},
title     = {A_Title},
}"""


@pytest.fixture
def entry_obj():
    parser_obj = Parser()
    file_path = os.path.join("BibTexTools", "tests", "data", "authors_abbreviate.bib")
    parsed_bibtex = parser_obj.from_file(file_path)
    entry = parsed_bibtex.entries[0]
    return entry


@pytest.fixture
def entry_obj_full():
    with pytest.warns(UserWarning):
        parser_obj = Parser()
        file_path = os.path.join("BibTexTools", "tests", "data", "full.bib")
        parsed_bibtex = parser_obj.from_file(file_path)
        entry = parsed_bibtex.entries[0]
    return entry


@pytest.fixture
def empty_entry():
    entry = Entry()
    return entry


class TestClassEntety:
    def test_add_field(self, empty_entry):
        empty_entry.add_field("year", "2020")
        assert empty_entry.year.value == "2020"
        assert empty_entry.year.name == "year"

    def test_add_nonstandard_field(self, empty_entry):
        with pytest.warns(UserWarning):
            empty_entry.add_field("my_field", "value")
        assert empty_entry.my_field.value == "value"
        assert empty_entry.my_field.name == "my_field"

    def test_add_author_field(self, empty_entry):
        empty_entry.add_field("author", "{first mid last}")
        assert isinstance(empty_entry.author, Author_field)
        assert isinstance(empty_entry.author.author_list[0], Author)
        assert empty_entry.author.author_list[0].first == "first"
        assert empty_entry.author.author_list[0].mid == ["mid"]
        assert empty_entry.author.author_list[0].last == "last"

    def test_add_journal(self, empty_entry):
        empty_entry.add_field("journal", "my_journal")
        assert isinstance(empty_entry.journal, Journal_field)

    def test_author_abbreviation(self, entry_obj):
        entry_obj = entry_obj.abbreviate_names(middle=True)

        assert entry_obj.author.author_list[0].name_short == "A1_Last, A. B."
        assert entry_obj.author.author_list[1].name_short == "A2_Last, A. B."
        assert entry_obj.author.author_list[2].name_short == "A3_Last, A. III."
        assert entry_obj.author.author_list[3].name_short == "A4_Last, A. B. Jr."

    def test_to_bibtex(self, entry_obj_full):
        bibtex_str = entry_obj_full.to_bibtex()
        assert bibtex_str.replace(" ", "") == A_string.replace(" ", "")

    def test_to_bibtex_fields(self, entry_obj_full):
        fields = ["type", "author", "title"]
        bibtex_str = entry_obj_full.to_bibtex(fields)
        assert bibtex_str.replace(" ", "") == A_string_fields.replace(" ", "")

    def test_to_dict(self, entry_obj_full):
        ref_dict = {
            "Akey": {
                "type": "Atype",
                "author": "A1_First von A1_Last and von A2_Last, A2_First",
                "title": "A_Title",
                "journal": "A_Journal",
                "volume": "A_Volume",
                "year": "A_Year",
                "url": "A_Url",
            }
        }
        entry_dict = entry_obj_full.to_dict()
        assert ref_dict == entry_dict

    def test_to_dict_fields(self, entry_obj_full):
        fields = ["type", "author", "title"]
        entry_dict = entry_obj_full.to_dict(fields)
        assert len(entry_dict["Akey"].keys()) == 3
        assert set(entry_dict["Akey"].keys()) == set(fields)
