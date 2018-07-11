from nltk.tokenize import sent_tokenize
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


def chunk_hansard_debate_file_nltk(file_path):
    """
    Try TextBlob to segment a Hansard debate into its constituent sentences.
    file_path e.g. "processed_hansard_data/1948-04-19/Oral Answers to Questions &#8212; Oyster Industry.txt"
    :param file_path:
    :return:
    """
    with open(file_path) as f:
        debate_text = f.read()

    sents = sent_tokenize(debate_text)
    print("Chunking up file: {}".format(file_path))
    dest_file_path = file_path \
        .replace("processed_hansard_data", "chunked_hansard_data") \
        .replace(".txt", "")
    for sentence_number, sentence in enumerate(sents):
        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        with open("{}-chunk-{}.txt"
                  .format(dest_file_path, sentence_number), "w+") as f:
            f.write(sentence)


def list_processed_hansard_files() -> List[str]:
    for _file in glob.glob("hansard_gathering/processed_hansard_data/**/*.txt", recursive=True):
        yield _file


def chunk_all_hansard_files():
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for _file in list_processed_hansard_files():
            # TODO try other chunking approaches: fixed-length, NLTK
            executor.submit(chunk_hansard_debate_file_nltk, _file)


