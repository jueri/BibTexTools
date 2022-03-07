import os

import pytest
from BibTexTools.cleaner import Cleaner
from BibTexTools.parser import Parser


@pytest.fixture
def cleaner_obj_simple():
    cleaner = Cleaner()
    return cleaner


@pytest.fixture
def cleaner_obj_keep_keys():
    cleaner = Cleaner(keep_keys=True)
    return cleaner


@pytest.fixture
def cleaner_obj_keep_unknown():
    cleaner = Cleaner(keep_unknown=True)
    return cleaner


@pytest.fixture
def cleaner_obj_ignore_unknown():
    cleaner = Cleaner(keep_unknown=False)
    return cleaner


@pytest.fixture
def bib_bert():
    bert_path = os.path.join("BibTexTools", "tests", "data", "bert.bib")
    parser = Parser()
    bert_bib = parser.from_file(bert_path)
    return bert_bib


@pytest.fixture
def bib_bert_short():
    bert_path = os.path.join("BibTexTools", "tests", "data", "bib_bert_short.bib")
    parser = Parser()
    bert_bib = parser.from_file(bert_path)
    return bert_bib


@pytest.fixture
def bib_unknown():
    bib_unknown = os.path.join("BibTexTools", "tests", "data", "bib_unknown.bib")
    parser = Parser()
    bib_unknown = parser.from_file(bib_unknown)
    return bib_unknown


class TestClassCleaner:
    def test_clean_simple(self, cleaner_obj_simple, bib_bert_short):
        with pytest.warns(UserWarning):
            cleaned_bib = cleaner_obj_simple.clean(bib_bert_short)
        cleaned_entry = cleaned_bib.entries[0]
        assert cleaned_entry.year.value == "{2019}"
        assert cleaned_entry.key.value == "DBLP:conf/naacl/DevlinCLT19"
        assert (
            cleaned_entry.publisher.value
            == r"{Association for Computational Linguistics}"
        )

    def test_clean_keep_keys(self, cleaner_obj_keep_keys, bib_bert_short):
        with pytest.warns(UserWarning):
            cleaned_bib = cleaner_obj_keep_keys.clean(bib_bert_short)
        cleaned_entry = cleaned_bib.entries[0]
        assert cleaned_entry.year.value == "{2019}"
        assert cleaned_entry.key.value == "devlin2018bert"
        assert (
            cleaned_entry.publisher.value
            == r"{Association for Computational Linguistics}"
        )

    def test_keep_unknown(self, cleaner_obj_keep_unknown, bib_unknown):
        with pytest.warns(UserWarning):
            cleaned_bib = cleaner_obj_keep_unknown.clean(bib_unknown)
        assert len(cleaned_bib.entries) == 2
        assert cleaned_bib.entries[0].key.value == "DBLP:conf/naacl/DevlinCLT19"
        assert cleaned_bib.entries[1].key.value == "unknown"

    def test_ignore_unknown(self, cleaner_obj_ignore_unknown, bib_unknown):
        with pytest.warns(UserWarning):
            cleaned_bib = cleaner_obj_ignore_unknown.clean(bib_unknown)
        assert len(cleaned_bib.entries) == 1
        assert cleaned_bib.entries[0].key.value == "DBLP:conf/naacl/DevlinCLT19"
