from typing import Generator, List, Tuple
from os import listdir
"""
A file for manipulating Hansard files on the filesystem, mainly to power the simple_gui
website.
"""


def get_dates_list() -> List[str]:
    """
    return a list of all Hansard dates available on this machine, from the filesystem.
    :return:
    """
    dates = listdir("hansard_gathering/processed_hansard_data")
    return sorted([_file for _file in dates if not _file.endswith("_num")])


def get_debates_by_date(date: str) -> Generator[Tuple[int, str], None, None]:
    debates = sorted(listdir("hansard_gathering/processed_hansard_data/{}".format(date)))
    filtered_debates: List[str] = [_file for _file in debates if not _file.endswith("-spans.txt")]
    for idx, debate in enumerate(filtered_debates):
        if not debate.endswith("-spans.txt"):
            yield (idx, debate)
