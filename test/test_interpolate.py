from typing import Set
from nltk.tokenize import TreebankWordTokenizer  # type: ignore
from hansard_gathering.interpolate import interpolate_one
from hansard_gathering.interpolate import ngram_span_search_named_entities


def test_interpolate_one(fs):
    all_places: Set[str] = {"London", "New York", "Las Vegas"}

    all_people: Set[str] = {"Margaret Thatcher", "Ernest Hemingway"}

    all_companies: Set[str] = ["Sainsburys", "Tescos", "The White House"]

    tokenizer = TreebankWordTokenizer()
    file_contents = "I do recall that Margaret Thatcher was good at finding Sainsburys in London"
    file_path = './hansard_gathering/processed_hansard_data/1976-02-09/Abortion (Amendment) Bill' \
        + ' (Select Committee).txt'

    interpolated_file_path = './hansard_gathering/interpolated_hansard_data/1976-02-09/Abortion ' \
        + '(Amendment) Bill (Select Committee).txt'

    fs.create_file(file_path, contents=file_contents)
    fs.create_file(interpolated_file_path, contents="")

    interpolate_one(file_path, tokenizer, "processed", all_places, all_companies, all_people)

    with open(interpolated_file_path) as f:
        contents = f.read()
        assert contents == "000000000000000003333333333333333300000000000000000000022222222220000111111"


def test_ngram_span_search_named_entities():
    span_window = ((20, 33), (34, 42), (43, 47), (48, 53))
    text = 'I have searched the International Monetary Fund rules, and I cannot find under which rule this is done.'
    all_places = {"Qatar"}
    all_companies = {"Sainsburys", "International Monetary Fund"}
    all_people = {"Ed Milliband"}
    result = ngram_span_search_named_entities(span_window, text, all_places, all_companies, all_people)
    expected_result = 20, 47, 2
    assert result == expected_result


