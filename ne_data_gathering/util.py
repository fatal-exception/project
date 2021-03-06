from typing import List, Set, Generator, Dict, Any
from os.path import realpath, dirname
from nltk.corpus import stopwords  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore

import os
import re

conll_file = 'raw_ne_data/eng.list'


def capitalise_text_list(l: List[str]) -> List[str]:
    new_list = []

    def capitalise(text: str):
        return text[:1].upper() + text[1:].lower()

    for elem in l:
        new_elem = " ".join([capitalise(word) for word in elem.split()])
        new_list.append(new_elem)

    return new_list


def write_to_data_file(data: List[str], category: str, file_name: str) -> None:
    file_path = realpath(__file__)
    data_path = "{}/processed_ne_data/{}/{}".format(dirname(file_path), category, file_name)
    os.makedirs(dirname(data_path), exist_ok=True)
    with open(data_path, "w+") as f:
        f.write("\n".join(data))
        f.write("\n")


def dbpedia_do_sparql_query(sparql_query: str) -> Dict[Any, Any]:
    from SPARQLWrapper import SPARQLWrapper, JSON  # type: ignore
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def process_conll_file(filepath, tag) -> Generator[str, None, None]:
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            contents = line.split(" ")
            if contents[0] == tag:
                yield " ".join(contents[1:]).rstrip()


def surrounded_by_chars(_line: str, start_char, end_char=None) -> bool:
    if end_char is None:
        end_char = start_char
    return _line.startswith(start_char) and _line.rstrip().endswith(end_char)


def remove_outer_brackets(_line: str) -> str:
    return _line[1:-2] + _line[-1]


def all_stop_words(line, stop_words: Set[str]) -> bool:
    line_words = word_tokenize(line)
    if all(word in stop_words for word in line_words):
        return True
    else:
        return False


def dbpedia_post_processing(src_list_file, dest_list_file):

    src_list_file = "ne_data_gathering/{}".format(src_list_file)

    stop_words = set(stopwords.words('english'))

    debug = False

    res_lines = []
    processed_list_file = "ne_data_gathering/{}".format(dest_list_file)

    with open(src_list_file, 'r+', encoding='utf-8') as f:
        lines = sorted(set(f.readlines()))

    for line in lines:
        # Remove double quotes
        line = line.replace('"', '')

        # Left-trim any whitespace
        line = line.lstrip()

        # Get rid of lines that are entirely numbers or symbols
        if re.match("""^[!@£$%^&*()0-9 ]+$""", line):
            print("DEBUG: Removing symbol lines {}".format(line)) if debug else None
            continue

        # If whole line is surrounded by brackets, remove those brackets
        if line.startswith("(") and line.endswith(")\n"):
            print("DEBUG: found bracketed line: {}".format(line)) if debug else None
            line = line[1:-2] + "\n"

        # If line starts with more than one single quote, remove all the single quotes at start
        match = re.match("""^'{2,}(.*)""", line)
        if match is not None:
            print("DEBUG: remove extraneous prefixed single quotes in line {}".format(line)) if debug\
                else None
            line = match.group(1)

        # If line ends with more than one single quote, remove all the single quotes at start
        match = re.match("""(.*)'{2,}$""", line)
        if match is not None:
            print("DEBUG: remove extraneous suffixed single quotes in line {}".format(line)) if debug \
                else None
            line = match.group(1) + "\n"

        # If line starts with just whitespace and/or asterisks, remove them
        match = re.match("""^[* ]+(.*)""", line)
        if match is not None:
            print("DEBUG: remove extraneous prefixed spaces/asterisks in line {}".format(line)) \
                if debug else None
            line = match.group(1)

        # Remove words shorter than 4 chars (they all have final newline)
        # These tend to be strange stub words like 'ar' which are low-value and hard to filter.
        if len(line) < 5:
            print("DEBUG: Removing short line {}".format(line)) if debug else None
            continue

        # If all words in the line are stop words, remove the line
        if all_stop_words(line, stop_words):
            continue

        res_lines.append(line)

    with open(processed_list_file, 'w+') as f:
        f.writelines(res_lines)
