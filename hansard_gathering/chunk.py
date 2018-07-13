from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from textblob import TextBlob
from typing import List
import concurrent.futures
import glob
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
    with open(file_path) as f:
        debate_text = f.read()

    sents = tokenizer.tokenize(debate_text)
    print("Chunking up file: {}".format(file_path))
    print("DEBUG: sents is {}".format(sents))
    dest_file_path = file_path \
        .replace("processed_hansard_data", "chunked_hansard_data") \
        .replace(".txt", "")
    for sentence_number, sentence in enumerate(sents):
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        with open("{}-chunk-{}.txt"
                  .format(dest_file_path, sentence_number), "w+") as f:
            f.write(sentence)


def list_processed_hansard_files() -> List[str]:
    print("Listing processed Hansard files...")
    for _file in glob.glob("hansard_gathering/processed_hansard_data/**/*.txt", recursive=True):
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


def chunk_all_hansard_files():
    tokenizer = nltk_get_tokenizer()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for _file in list_processed_hansard_files():
            # TODO try other chunking approaches: fixed-length
            executor.submit(chunk_hansard_debate_file_nltk, _file, tokenizer)


