from nltk.tokenize import TreebankWordTokenizer
from hansard_gathering.interpolate import interpolate_one
import os


def test_interpolate_one(fs):
    all_places = """
    London
    New York
    Las Vegas
    """

    all_people = """
    Margaret Thatcher
    Ernest Hemingway
    """

    all_companies = """
    Sainsburys
    Tescos
    The White House
    """

    tokenizer = TreebankWordTokenizer()
    file_contents = "I do find that Margaret Thatcher was good at finding Sainsburys in London"
    file_path = '/hansard_gathering/chunked_hansard_data/1976-02-09/Abortion (Amendment) Bill' \
                + '(Select Committee)-chunk-995.txt'

    interpolated_file_path = '/hansard_gathering/interpolated_hansard_data/1976-02-09/Abortion ' \
                             + '(Amendment) Bill (Select Committee)-chunk-995.txt'

    fs.create_file(file_path, contents=file_contents)
    fs.create_file(interpolated_file_path, contents="")

    interpolate_one(file_path, tokenizer, all_places, all_companies, all_people)

    with open(interpolated_file_path) as f:
        contents = f.read()
        print(contents)
        assert len(contents) > 0
