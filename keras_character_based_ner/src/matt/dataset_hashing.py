import os
import glob
from collections import defaultdict
from typing import List


def get_total_number_of_buckets() -> int:
    return 320


def get_bucket_numbers_for_dataset_name(dataset_name: str) -> List[int]:
    """
    Function to control bucket quantities and relative sizes of datasets
    :param dataset_name: ALL, train, dev or test
    :return: a list of ints for the bucket numbers containing file lists
    which, when unioned together, comprise that dataset.
    """
    # Keeping ALL artificially small for now while we get the model working.
    if dataset_name == "ALL":
        return list(range(8))
    elif dataset_name == "train":
        return list(range(0, 4))
    elif dataset_name == "dev":
        return list(range(4, 6))
    elif dataset_name == "test":
        return list(range(6, 8))
    # Small set of debates to build an alphabet off
    elif dataset_name == "alphabet-sample":
        return [0]
    else:
        return []


def archive_old_bucket_allocations():
    """
    Move old bucket files in hansard_gathering/data_buckets to an archive so they're not lost
    """
    os.makedirs("hansard_gathering/data_buckets_archive", exist_ok=True)

    file_list = sorted(glob.glob("hansard_gathering/data_buckets/*.txt"))
    for _file in file_list:
        new_dest = _file.replace("data_buckets", "data_buckets_archive")
        os.rename(_file, new_dest)


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

    archive_old_bucket_allocations()

    # bucket allocations: 4 for train, 2 for dev, 2 for test
    num_of_buckets: int = get_total_number_of_buckets()
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


