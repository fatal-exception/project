from datetime import datetime
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from textblob import TextBlob
from typing import List
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
    dest_file_path = file_path \
        .replace("processed_hansard_data", "chunked_hansard_data") \
        .replace(".txt", "")

    with open(file_path) as f:
        debate_text = f.read()

    sents = tokenizer.tokenize(debate_text)
    print("Chunking up file: {}".format(file_path))
    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
    for sentence_number, sentence in enumerate(sents):
        with open("{}-chunk-{}.txt"
                  .format(dest_file_path, sentence_number), "w+") as f:
            f.write(sentence)
    os.remove(file_path)


def list_processed_hansard_files(starting_date) -> List[str]:
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
    abbreviation = ['hon', 'mr', 'mrs']
    punkt_param.abbrev_types = set(abbreviation)
    return PunktSentenceTokenizer(punkt_param)


def chunk_all_hansard_files(starting_date):
    tokenizer = nltk_get_tokenizer()
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        for _file in list_processed_hansard_files(starting_date):
            # TODO try other chunking approaches: fixed-length
            executor.submit(chunk_hansard_debate_file_nltk, _file, tokenizer)


