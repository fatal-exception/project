from datetime import datetime
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters  # type: ignore
from typing import Generator, Tuple
import concurrent.futures
import glob
import itertools
import os


def chunk_hansard_debate_file_textblob(file_path):
    """
    Try TextBlob to segment a Hansard debate into its constituent sentences.
    file_path e.g. "processed_hansard_data/1948-04-19/Oral Answers to Questions &#8212; Oyster Industry.txt"
    :param file_path:
    :return:
    """
    from textblob import TextBlob  # type: ignore

    with open(file_path) as f:
        debate_text = f.read()

    tb = TextBlob(debate_text)
    print("Chunking up file: {}".format(file_path))
    dest_file_path = file_path\
        .replace("processed_hansard_data", "chunked_hansard_data")\
        .replace(".txt", "")
    for sentence_number, sentence in enumerate(tb.sentences):
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        with open("{}-chunk-{}.txt"
                  .format(dest_file_path, sentence_number), "w+") as f:
            f.write(sentence.raw)


def chunk_hansard_debate_file_nltk(file_path, tokenizer):
    """
    Try NLTK to segment a Hansard debate into its constituent sentences.
    file_path e.g. "processed_hansard_data/1948-04-19/Oral Answers to Questions &#8212; Oyster Industry.txt"
    :param file_path: path of file to split up
    :param tokenizer: An NLTK tokenizer with customisations for Hansard
    """
    dest_file_path = file_path.replace(".txt", "-spans.txt")

    with open(file_path) as f:
        debate_text = f.read()

    print("Chunking up file: {}".format(file_path))
    sent_spans = tokenizer.span_tokenize(debate_text)
    sent_spans_str = "\n".join("({},{})".format(
        sent_start, sent_end) for sent_start, sent_end in sent_spans)
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    with open(dest_file_path, "w+") as f:
        f.write(sent_spans_str)


def list_processed_hansard_files(starting_date) -> Generator[str, None, None]:
    """
    Provide a starting_date as chunking takes a long time. This allows the process to be resumable.
    :param starting_date: e.g. 1919-01-01
    :return:
    """
    print("Listing processed Hansard files...")
    files = sorted(glob.glob("hansard_gathering/processed_hansard_data/**/*.txt", recursive=True))

    # With thanks to
    # https://stackoverflow.com/questions/33895760/python-idiomatic-way-to-drop-items-from-a-list-until-an-item-matches-a-conditio
    def date_is_less_than_starting_date(file_path):
        file_path_date = file_path.split("/")[2]
        file_path_dt = datetime.strptime(file_path_date, "%Y-%M-%d")
        starting_dt = datetime.strptime(starting_date, "%Y-%M-%d")
        return file_path_dt < starting_dt

    filtered_files = list(itertools.dropwhile(date_is_less_than_starting_date, files))
    for _file in filtered_files:
        yield _file


def nltk_get_tokenizer():
    """
    Return a tokenizer with some customization for Hansard
    :return:  a Punkt tokenizer
    """
    # With thanks to
    # https://stackoverflow.com/questions/34805790/how-to-avoid-nltks-sentence-tokenizer-spliting-on-abbreviations
    punkt_param = PunktParameters()
    # 'hon. Gentleman' is very common in Hansard!
    abbreviation = ['hon', 'mr', 'mrs', 'no']
    punkt_param.abbrev_types = set(abbreviation)
    return PunktSentenceTokenizer(punkt_param)


def chunk_all_hansard_files(starting_date):
    tokenizer = nltk_get_tokenizer()
    pool_implementation = concurrent.futures.ProcessPoolExecutor
    # pool_implementation = concurrent.futures.ThreadPoolExecutor
    with pool_implementation(max_workers=16) as executor:
        for _file in list_processed_hansard_files(starting_date):
            # TODO try other chunking approaches: fixed-length
            executor.submit(chunk_hansard_debate_file_nltk, _file, tokenizer)


def get_sentence_spans(filepath) -> Generator[Tuple[int, int], None, None]:
    with open("{}.txt".format(filepath.replace(".txt", "-spans"))) as f:
        sent_spans = f.read()

    for sent_span in sent_spans.split("\n"):
        sent_start, sent_end = sent_span.replace("(", "").replace(")", "").split(",")
        yield int(sent_start), int(sent_end)


def display_chunked_hansard(filepath):
    assert "processed_hansard_data" in filepath, \
        "We only allow processed hansards to be displayed in chunks"

    with open(filepath) as f:
        debate = f.read()

    for sent_start, sent_end in get_sentence_spans(filepath):
        print(debate[int(sent_start):int(sent_end)])
        print("@@@")

