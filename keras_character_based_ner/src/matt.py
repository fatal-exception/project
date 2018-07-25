# MIR file added to provide integration with Keras
from collections import defaultdict
import glob
import numpy as np  # type: ignore
import os
import pickle
from keras_character_based_ner.src.alphabet import CharBasedNERAlphabet
from typing import Dict, Generator, List, Set, Tuple
from hansard_gathering import numerify, chunk


def get_bucket_numbers_for_dataset_name(dataset_name: str) -> List[int]:
    """
    Function to control bucket quantities and relative sizes of datasets
    :param dataset_name: ALL, train, dev or test
    :return: a list of ints for the bucket numbers containing file lists
    which, when unioned together, comprise that dataset.
    """
    if dataset_name == "ALL":
        return list(range(8))
    elif dataset_name == "train":
        return list(range(0, 4))
    elif dataset_name == "dev":
        return list(range(4, 6))
    elif dataset_name == "test":
        return list(range(6, 8))
    else:
        return []  # to keep mypy static type-checker happy


def rehash_datasets():
    """
    Hash all Hansard debates into 3 datasets:
    train
    test
    dev
    (ALL)
    We take a hash of the date-and-debate-name part of each filepath, then use modulo to
    bucket this.
    """
    # bucket allocations: 4 for train, 2 for dev, 2 for test
    num_of_buckets: int = len(get_bucket_numbers_for_dataset_name("ALL"))
    debug: bool = True

    os.makedirs("hansard_gathering/data_buckets", exist_ok=True)
    Filepaths = Set[str]
    BucketNumber = int
    files_by_bucket: Dict[BucketNumber, Filepaths] = defaultdict(lambda: set())

    file_list = sorted(glob.glob(
        "hansard_gathering/processed_hansard_data/**/*.txt", recursive=True))

    file_list = list(filter(lambda elem: not elem.endswith("-spans.txt"), file_list))

    for _file in file_list:
        date_filename_path: str = "/".join(_file.split("/")[2:])
        hash_val: int = hash(date_filename_path)
        bucket_num = hash_val % num_of_buckets
        files_by_bucket[bucket_num].add(_file)
        print("hashed {} into bucket {}".format(_file, bucket_num)) if debug else None

    for bucket_num in files_by_bucket.keys():
        with open("hansard_gathering/data_buckets/{}.txt".format(bucket_num), "w") as f:
            filepaths = sorted(files_by_bucket[bucket_num])
            for filepath in filepaths:
                f.write(filepath + "\n")


def get_all_hansard_files(dataset_name: str):
    """
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


def get_some_hansard_files(stage="processed"):
    """
    For testing on smaller dataset.
    Stage is processed or chunked.
    """
    print("Starting glob for some processed Hansard files")
    for _file in sorted(glob.glob(
            "hansard_gathering/{}_hansard_data/1994*/*.txt".format(stage), recursive=True)):
        yield _file


def get_some_texts() -> Generator[str, None, None]:
    for _file in get_some_hansard_files("processed"):
        print("Getting text from {}".format(_file))
        yield open(_file).read()


def get_texts() -> Generator[str, None, None]:
    for _file in get_all_hansard_files("ALL"):
        print("Getting text from {}".format(_file))
        yield open(_file).read()


def get_alphabet():
    return CharBasedNERAlphabet.get_alphabet_from_texts(get_texts())


def get_some_alphabet():
    return CharBasedNERAlphabet(get_some_texts())


def pickle_some_alphabet():
    alph = get_some_alphabet()
    with open("keras_character_based_ner/src/some_alphabet.p", "wb") as f:
        pickle.dump(alph, f)


def display_pickled_alphabet():
        alph = get_pickled_alphabet()
        print(alph)
        for i, ch in enumerate(alph):
            print("{}: {}".format(i, ch))


def get_pickled_alphabet():
    with open("keras_character_based_ner/src/some_alphabet.p", "rb") as f:
        return pickle.load(f)


def get_labels():
    # 1 = LOC, 2 = ORG, 3 = PER, 0 = null
    return list(range(1, 4))


def get_chunked_hansard_texts(dataset_name: str) -> Generator[str, None, None]:
    """
    :param dataset_name: dev, test or train
    Generator that goes over all Hansard debate files and returns their next sentence, using their spans file.
    :return:
    """
    for _file in get_all_hansard_files(dataset_name):
        with open(_file) as f:
            debate = f.read()
            chunk_start: int
            chunk_end: int
        for chunk_start, chunk_end in chunk.get_sentence_spans(_file):
            yield debate[chunk_start:chunk_end]


def get_hansard_span_files(dataset_name: str) -> Generator[str, None, None]:
    print("Listing Hansard span files from dataset {}...".format(dataset_name))
    bucket_numbers: List[int] = get_bucket_numbers_for_dataset_name(dataset_name)
    file_list = []
    for bucket_number in bucket_numbers:
        with open("hansard_gathering/data_buckets/{}.txt".format(bucket_number)) as f:
            file_list.extend([filename.rstrip().replace(".txt", "-spans.txt") for filename in f.readlines()])
    for span_file in file_list:
        yield span_file


def file_lines(fname: str) -> int:
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


def create_x(sentence_maxlen, dataset_name):
    debug: bool = True

    total_chunks: int = 0
    if debug:
        total_chunks = read_total_number_of_hansard_sentences_from_file(dataset_name)

    from keras.preprocessing.sequence import pad_sequences  # type: ignore
    alphabet = get_pickled_alphabet()

    x_list: List[List[int]] = []
    for idx, hansard_sentence in enumerate(get_chunked_hansard_texts(dataset_name)):
        numbers_list: List[int] = numerify.numerify_text(hansard_sentence, alphabet)
        x_list.append(numbers_list)
        if debug:
            print("Building x, progress {} %".format(idx / total_chunks)) if idx % 10000 == 0 else None

    # pad_sequences takes care of enforcing sentence_maxlen for us
    x_np = pad_sequences(x_list, maxlen=sentence_maxlen)

    # Write X so we don't have to regenerate every time...
    with open("keras_character_based_ner/src/x-{}.p".format(dataset_name), "wb") as f:
        f.write(x_np)


def get_x_y(sentence_maxlen, dataset_name) -> Tuple:
    """
    Returns a Python tuple x and y, where x and y are Numpy arrays!
                x: Array of shape (batch_size, sentence_maxlen).
                Entries in dimension 1 are alphabet indices, index 0 is the padding symbol
                y: Array of shape (batch_size, sentence_maxlen, self.num_labels).
                Entries in dimension 2 are label indices, index 0 is the null label
                I guess batch_size here refers to the WHOLE batch?
    """
    with open("keras_character_based_ner/src/matt/x-{}.p".format(dataset_name), "rb") as f:
        x_np = f.read()

    return x_np, None


def get_x_y_generator():
    """
    Generator that returns a tuple each time, of inputs/targets as Numpy arrays. Each tuple
    is a batch used in training.
    :return: Generator object that yields tuples (x, y), same as in get_x_y()
    """
    pass
