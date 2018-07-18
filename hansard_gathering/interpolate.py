from nltk.tokenize import TreebankWordTokenizer
from nltk import ngrams
import os


def get_all_ne_data():
    with open("ne_data_gathering/processed_ne_data/places/ALL.txt") as f:
        all_places = [line.rstrip() for line in f]
    with open("ne_data_gathering/processed_ne_data/companies/ALL.txt") as f:
        all_companies = [line.rstrip() for line in f]
    with open("ne_data_gathering/processed_ne_data/people/ALL.txt") as f:
        all_people = [line.rstrip() for line in f]

    return all_places, all_companies, all_people


def interpolate_one(file_path, tokenizer, all_places, all_companies, all_people, n=4):
    """
    file_path e.g. hansard_gathering/chunked_hansard_data/1943-09-21/Deaths of Members-chunk-1979.txt
    :param file_path: path to file to do interpolation on
    :param tokenizer: an NLTK tokenizer with span_tokenize method
    :param all_*: files with lists of _all_ collected examples of that NE type, \n-separated
    :param n: number to use for ngramming
    :return: None (we write out to disk)
    """
    with open(file_path) as f:
        text = f.read()
        interpolated_text = "0" * len(text)

    # ngrams for the text that capture their starting and ending indices
    text_span_ngrams = ngrams(tokenizer.span_tokenize(text), n)

    # For each ngram set, we want to try all possible suffixes against the NE lists,
    # from longest to shortest so we don't miss matches.
    # Once we find a match, move on to the next ngram.
    for ngram_span_window in text_span_ngrams:
        match_start: int
        match_end: int
        ne_type: int # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
        match_start, match_end, ne_type = ngram_span_search_named_entities(
            ngram_span_window, all_places, all_companies, all_people)
        if ne_type is not 0:
            # Build new interpolated text by adding NE markers using concatenation
            # TODO
            match_len = match_end - match_start
            interpolated_text = interpolated_text[:match_start] + ne_type * match_len + interpolated_text[match_end:]

    interpolated_file_path = file_path.replace("chunked_hansard_data", "interpolated_hansard_data")
    os.makedirs(os.path.dirname(interpolated_file_path), exist_ok=True)
    with open(interpolated_file_path, "w") as f:
        f.write(interpolated_text)


def interpolate_one_wrapper(file_path):
    t = TreebankWordTokenizer()
    interpolate_one(file_path, t, *get_all_ne_data())
