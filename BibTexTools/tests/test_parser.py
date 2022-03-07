import pytest
import os
from BibTexTools.parser import Parser


@pytest.fixture
def bib_simple():
    with open(os.path.join("BibTexTools", "tests", "data", "simple.bib"), "r") as fin:
        bibtex_string = fin.read()
    return bibtex_string


@pytest.fixture
def parser_obj():
    return Parser()


class TestClassParser:
    def test_parse_len(self, parser_obj, bib_simple):
        parsed_bibtex = parser_obj.parse(bib_simple)
        assert isinstance(parsed_bibtex.entries, list)
        assert len(parsed_bibtex.entries) == 1

    def test_parse_from_string(self, parser_obj, bib_simple):
        parsed_bibtex = parser_obj.parse(bib_simple)
        entry = parsed_bibtex.entries[0]

        assert entry.key.value == "key"
        assert entry.type.value == "type"
        assert entry.journal.value == r"{myjournal}"
        assert entry.title.value == r"{mytitle}"

    def test_file_not_exists(self, parser_obj):
        with pytest.raises(FileNotFoundError):
            parser_obj.from_file("not_there.bib")

    def test_parse_from_file(self, parser_obj):
        file_path = os.path.join("BibTexTools", "tests", "data", "simple.bib")
        parsed_bibtex = parser_obj.from_file(file_path)
        entry = parsed_bibtex.entries[0]

        assert entry.key.value == "key"
        assert entry.type.value == "type"
        assert entry.journal.value == r"{myjournal}"
        assert entry.title.value == r"{mytitle}"

    def test_not_standard_field(self, parser_obj):
        file_path = os.path.join("BibTexTools", "tests", "data", "not_standard.bib")
        with pytest.warns(UserWarning):
            parser_obj.from_file(file_path)

    def test_authors(self, parser_obj):
        file_path = os.path.join("BibTexTools", "tests", "data", "authors.bib")
        parsed_bibtex = parser_obj.from_file(file_path)
        entry = parsed_bibtex.entries[0]

        assert entry.author.author_list[0].first == "A1_First"
        assert entry.author.author_list[0].last == "von A1_Last"
        assert entry.author.author_list[0].mid == []
        assert entry.author.author_list[1].first == "A2_First"
        assert entry.author.author_list[1].last == "von A2_Last"
        assert entry.author.author_list[1].mid == []
        assert entry.author.author_list[2].first == "A3_First"
        assert entry.author.author_list[2].last == "von A3_Last"
        assert entry.author.author_list[2].mid == ["A3_Jr"]
        assert entry.author.author_list[3].first == "A4_First"
        assert entry.author.author_list[3].last == "A4_Last"
        assert entry.author.author_list[3].mid == ["A4_Mid", "A4_Mid2"]

    def test_authors_abbreviate(self, parser_obj):
        file_path = os.path.join(
            "BibTexTools", "tests", "data", "authors_abbreviate.bib"
        )
        parsed_bibtex = parser_obj.from_file(file_path)
        entry = parsed_bibtex.entries[0]

        assert entry.author.author_list[0].first == "A1_First"
        assert entry.author.author_list[0].last == "A1_Last"
        assert entry.author.author_list[0].mid == ["B1_Mid"]

        assert entry.author.author_list[1].first == "A2_First"
        assert entry.author.author_list[1].last == "A2_Last"
        assert entry.author.author_list[1].mid == ["B."]

        assert entry.author.author_list[2].first == "A3_First III."
        assert entry.author.author_list[2].last == "A3_Last"
        assert entry.author.author_list[2].mid == []

        assert entry.author.author_list[3].first == "A4_First"
        assert entry.author.author_list[3].last == "A4_Last Jr."
        assert entry.author.author_list[3].mid == ["B4_Mid"]
