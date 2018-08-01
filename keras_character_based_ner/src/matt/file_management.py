from typing import List, Generator, Any
import os
import pickle
from keras_character_based_ner.src.matt.dataset_hashing import get_bucket_numbers_for_dataset_name
from hansard_gathering import chunk


def get_all_hansard_files(dataset_name: str) -> Generator[str, None, None]:
    """
    Return generator of all file names in a given dataset.
    :param dataset_name: train, dev, test or ALL
    :return:
    """
    print("Listing Hansard debate files from dataset {}...".format(dataset_name))
    bucket_numbers: List[int] = get_bucket_numbers_for_dataset_name(dataset_name)
    file_list = []
    for bucket_number in bucket_numbers:
        with open("hansard_gathering/data_buckets/{}.txt".format(bucket_number)) as f:
            file_list.extend([filename.rstrip() for filename in f.readlines()])
    for _file in file_list:
        yield _file


def get_hansard_span_files(dataset_name: str) -> Generator[str, None, None]:
    """
    For a given dataset name, yield just the span files (list of sentence starts
    and stops) for each debate in that dataset. Only used to get the total
    number of sentences in the dataset at present.
    :param dataset_name:
    :return:
    """
    print("Listing Hansard span files from dataset {}...".format(dataset_name))
    bucket_numbers: List[int] = get_bucket_numbers_for_dataset_name(dataset_name)
    file_list = []
    for bucket_number in bucket_numbers:
        with open("hansard_gathering/data_buckets/{}.txt".format(bucket_number)) as f:
            file_list.extend([filename.rstrip().replace(".txt", "-spans.txt") for filename in f.readlines()])
    for span_file in file_list:
        yield span_file


def file_lines(fname: str) -> int:
    """
    Fast implementation to get number of lines in a file - useful with span files,
    to count total number of different sentences.
    :param fname:
    :return:
    """
    # with thanks to
    # https://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    with open(fname) as f:
        i: int = 0
        for i, l in enumerate(f):
            pass
    return i + 1


def write_total_number_of_hansard_sentences_to_file(dataset_name: str):
    """
    Get num of sentences in a particular dataset, dev, test or train.
    Also accept dataset_name 'ALL' while I work on dataset divisions.
    Count number of sentences in the -spans files and write this out to
    disk to save time.

    :param dataset_name: must be dev, test or train
    :return:
    """
    # Run on 25 July 2018 this was 182582013
    sentences_total: int = 0
    for span_file in get_hansard_span_files(dataset_name):
        sentences_total += file_lines(span_file)

    with open("hansard_gathering/processed_hansard_data/{}_total_sentences_num".format(dataset_name), "w+") as f:
        f.write(str(sentences_total))


def read_total_number_of_hansard_sentences_from_file(dataset_name) -> int:
    """
    Get num of samples in a particular dataset, dev, test or train.
    Also accept dataset_name 'ALL' while I work on dataset divisions.
    Read this information from disk.
    :param dataset_name: must be dev, test or train
    :return:
    """
    with open("hansard_gathering/processed_hansard_data/{}_total_sentences_num".format(dataset_name), "r") as f:
        sentences = f.read()

    return int(sentences)


def get_chunked_hansard_interpolations(dataset_name: str) -> Generator[str, None, None]:
    """
    :param dataset_name: dev, test or train
    Generator that goes over all Hansard debate files and returns their next sentence worth of interpolation-numbers,
    using a span file.
    :return:
    """
    _file: str
    for _file in get_all_hansard_files(dataset_name):
        interpolations_file: str = _file.replace(
            "processed_hansard_data", "interpolated_hansard_data")
        with open(interpolations_file, "r") as f:
            interpolations_data: str = f.read()
            span_start: int
            span_end: int
            for span_start, span_end in chunk.get_sentence_spans(_file):
                yield interpolations_data[span_start:span_end]


def unpickle_large_file(filepath) -> Any:
    """
    See https://stackoverflow.com/questions/31468117/python-3-can-pickle-handle-byte-objects-larger-than-4gb
    MacOS has a bug which stops objects larger than 4GB from being written out to file. What a pain!
    :param filepath:
    :return:
    """
    max_bytes = 2**31 - 1
    bytes_in = bytearray(0)
    input_size = os.path.getsize(filepath)
    with open(filepath, 'rb') as f_in:
        for _ in range(0, input_size, max_bytes):
            bytes_in += f_in.read(max_bytes)
    return pickle.loads(bytes_in)


def pickle_large_file(data_structure, filepath):
    """
    See https://stackoverflow.com/questions/31468117/python-3-can-pickle-handle-byte-objects-larger-than-4gb
    MacOS has a bug which stops objects larger than 4GB from being written out to file. What a pain!
    :param data_structure:
    :param filepath:
    :return:
    """
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(data_structure, protocol=4)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, len(bytes_out), max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])


def get_texts() -> Generator[str, None, None]:
    """
    Return the texts from hansard files, without chunking into sentences. This
    is only required for the keras dataset to build an alphabet, so we only need
    to return a small subset. We make a bucket set called alphabet-sample for this.
    :return:
    """
    return get_chunked_hansard_texts("alphabet-sample")


def get_chunked_hansard_texts(dataset_name: str) -> Generator[str, None, None]:
    """
    :param dataset_name: dev, test or train
    Generator that goes over all Hansard debate files and returns their next sentence,
     using their spans file. This is required to build the X tensor - the resulting
    sentence-spans are each numerified before being turned into numpy arrays.
    :return:
    """
    for _file in get_all_hansard_files(dataset_name):
        with open(_file) as f:
            debate = f.read()
            chunk_start: int
            chunk_end: int
        for chunk_start, chunk_end in chunk.get_sentence_spans(_file):
            yield debate[chunk_start:chunk_end]
