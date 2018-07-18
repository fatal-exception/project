from nltk.tokenize import TreebankWordTokenizer
from nltk import ngrams
from typing import List
import concurrent.futures
import glob
import os


def get_all_ne_data():
    with open("ne_data_gathering/processed_ne_data/places/ALL.txt") as f:
        all_places = [line.rstrip() for line in f]
    with open("ne_data_gathering/processed_ne_data/companies/ALL.txt") as f:
        all_companies = [line.rstrip() for line in f]
    with open("ne_data_gathering/processed_ne_data/people/ALL.txt") as f:
        all_people = [line.rstrip() for line in f]

    return all_places, all_companies, all_people


def ngram_span_search_named_entities(ngram_span_window, text, all_places: List[str], all_companies: List[str], all_people: List[str]):
    """
    Take a window e.g.((0, 1), (2, 6), (7, 15), (16, 19)) from a text. Starting with the longest
    suffix (0-19 here), and working back via middle (e.g. 0-15) to the first (0-1),
    check all NE lists for the text bounded by these indices.
    If matches, return where the match started and ended, and which NE it is.
    Note that because we pad_right, later elements in the tuple might be None, e.g.:
    ((98, 102), (102, 103), None, None)
    :param ngram_span_window: As shown in example above, taken from span_tokenize.
    :param all_places: NE list
    :param all_companies: NE list
    :param all_people: NE list
    :return: match_start where match starts, match_end where match ends (half-open?), ne_type as int
    where 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    """
    start_index = ngram_span_window[0][0]
    for end_index in reversed([tup[-1] for tup in ngram_span_window if tup is not None]):
        if text[start_index:end_index] in all_places:
            return start_index, end_index, 1
        elif text[start_index:end_index] in all_companies:
            return start_index, end_index, 2
        elif text[start_index:end_index] in all_people:
            return start_index, end_index, 3

    return 0, 0, 0


def interpolate_one(
        file_path: str, tokenizer, all_places: List[str], all_companies: List[str], all_people: List[str], n=4):
    """
    file_path e.g. hansard_gathering/chunked_hansard_data/1943-09-21/Deaths of Members-chunk-1979.txt
    :param file_path: path to file to do interpolation on
    :param tokenizer: an NLTK tokenizer with span_tokenize method
    :param all_*: files with lists of _all_ collected examples of that NE type, \n-separated
    :param n: number to use for ngramming
    :return: None (we write out to disk)
    """
    print("Interpolating into {}".format(file_path))
    with open(file_path) as f:
        text: str = f.read()
        interpolated_text: str = "0" * len(text)

    # ngrams for the text that capture their starting and ending indices.
    # We pad right because we take the first word of the ngram and all its possible suffixes
    # when looking for NEs.
    text_span_ngrams = ngrams(tokenizer.span_tokenize(text), n, pad_right=True)

    # Returns ngrams of text_spans e.g. [((0, 1), (2, 6), (7, 15), (16, 19)), ...]

    # For each ngram set, we want to try all possible suffixes against the NE lists,
    # from longest to shortest so we don't miss matches.
    # Once we find a match, move on to the next ngram.
    for ngram_span_window in text_span_ngrams:
        match_start: int
        match_end: int
        ne_type: int  # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
        match_start, match_end, ne_type = ngram_span_search_named_entities(
            ngram_span_window, text, all_places, all_companies, all_people)
        if ne_type is not 0:
            # Build new interpolated text by adding NE markers using concatenation
            match_len = match_end - match_start
            interpolated_text = interpolated_text[:match_start] \
                + str(ne_type) * match_len \
                + interpolated_text[match_end:]

    interpolated_file_path = file_path.replace("chunked_hansard_data", "interpolated_hansard_data")
    os.makedirs(os.path.dirname(interpolated_file_path), exist_ok=True)
    with open(interpolated_file_path, "w") as f:
        f.write(interpolated_text)


def interpolate_one_wrapper(file_path):
    t = TreebankWordTokenizer()
    interpolate_one(file_path, t, *get_all_ne_data())


def list_chunked_hansard_files() -> List[str]:
    print("Listing chunked Hansard files...")
    for _file in glob.glob("hansard_gathering/chunked_hansard_data/**/*.txt", recursive=True):
        yield _file


def interpolate_all_hansard_files():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for _file in list_chunked_hansard_files():
            executor.submit(interpolate_one_wrapper, _file)
