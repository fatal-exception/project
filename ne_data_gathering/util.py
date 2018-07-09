from typing import List
from os.path import realpath, dirname

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


def dbpedia_do_sparql_query(sparql_query: str) -> str:
    from SPARQLWrapper import SPARQLWrapper, JSON
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results: str = sparql.query().convert()
    return results


def process_conll_file(filepath, tag) -> List[str]:
    with open(filepath) as f:
        lines: List[str] = f.readlines()
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


def dbpedia_post_processing(src_list_file, dest_list_file):

    res_lines = []
    processed_list_file = dest_list_file
    with open(src_list_file, 'r+', encoding='utf-8') as f:
        lines: List[str] = sorted(set(f.readlines()))
        for line in lines:
            # 1. Remove double quotes
            line = line.replace('"', '')
            # 2. Left-trim any whitespace
            line = line.lstrip()
            if line == "":
                continue
            # 3. Get rid of lines that are entirely numbers or symbols
            if re.match("""^\d+$""", line) or re.match("""^[!@£$%^&*()]+$""", line):
                continue
            res_lines.append(line)
    with open(processed_list_file, 'w+') as f:
        f.writelines(res_lines)
