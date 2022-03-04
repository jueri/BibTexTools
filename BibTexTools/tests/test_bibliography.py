import os
from BibTexTools.parser import Parser
import pytest
import json

Bib_string = """@Atype{Akey,
author    = {A1_First von A1_Last and
            von A2_Last, A2_First},
title     = {A_Title},
journal   = {A_Journal},
volume    = {A_Volume},
year      = {A_Year},
url       = {A_Url},
}


@Btype{Bkey,
author    = {B1_First von B1_Last and
            von B2_Last, B2_First},
title     = {B_Title},
journal   = {B_Journal},
volume    = {B_Volume},
year      = {B_Year},
url       = {B_Url},
}"""

Bib_string_fields = """@Atype{Akey,
author    = {A1_First von A1_Last and
            von A2_Last, A2_First},
title     = {A_Title},
}


@Btype{Bkey,
author    = {B1_First von B1_Last and
            von B2_Last, B2_First},
title     = {B_Title},
}"""


@pytest.fixture
def bib_obj_full():
    with pytest.warns(UserWarning):
        parser_obj = Parser()
        file_path = os.path.join("BibTexTools", "tests", "data", "full.bib")
        parsed_bibtex = parser_obj.from_file(file_path)
    return parsed_bibtex


class TestClassBibliography:
    def test_to_bibtex(self, bib_obj_full):
        bibtex_str = bib_obj_full.to_bibtex()
        assert bibtex_str.replace(" ", "") == Bib_string.replace(" ", "")

    def test_to_bibtex_fields(self, bib_obj_full):
        fields = ["author", "title"]
        bibtex_str = bib_obj_full.to_bibtex(fields)
        assert bibtex_str.replace(" ", "") == Bib_string_fields.replace(" ", "")

    def test_to_bib(self, bib_obj_full):
        file_path = os.path.join("BibTexTools", "tests", "data", "to_bib.bib")
        bib_obj_full.to_bib(file_path)
        assert os.path.isfile(file_path)
        os.remove(file_path)

    def test_to_bib_fields(self):
        pass
        # TODO

    def test_to_json_exists(self, bib_obj_full):
        file_path = os.path.join("BibTexTools", "tests", "data", "to_json.json")
        bib_obj_full.to_json(file_path)
        assert os.path.isfile(file_path)
        os.remove(file_path)

    def test_to_json_file(self, bib_obj_full):
        file_path = os.path.join("BibTexTools", "tests", "data", "to_json.json")
        bib_obj_full.to_json(file_path)
        with open(file_path, "r") as fin:
            new_file = json.load(fin)

        ref_file_path = os.path.join("BibTexTools", "tests", "data", "to_json_ref.json")
        with open(ref_file_path, "r") as fin:
            ref_file = json.load(fin)

        assert ref_file == new_file
        os.remove(file_path)

    def test_to_json_fields(self):
        pass
        # TODO
