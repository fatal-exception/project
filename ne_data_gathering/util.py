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

    debug = True

    res_lines = []
    processed_list_file = dest_list_file

    with open(src_list_file, 'r+', encoding='utf-8') as f:
        lines: List[str] = sorted(set(f.readlines()))

    for line in lines:
        # 1. Remove double quotes
        line = line.replace('"', '')

        # 2. Left-trim any whitespace
        line = line.lstrip()

        # 3. Remove words shorter than 4 chars (they all have final newline)
        # These tend to be wrong words like 'the' and are low-value and hard to filter.
        if len(line) < 5:
            print("DEBUG: Removing short line {}".format(line)) if debug else None
            continue

        # 4. Get rid of lines that are entirely numbers or symbols
        if re.match("""^[!@£$%^&*()0-9 ]+$""", line):
            print("DEBUG: Removing symbol lines {}".format(line)) if debug else None
            continue

        # 5. If whole line is surrounded by brackets, remove those brackets
        if line.startswith("(") and line.endswith(")\n"):
            print("DEBUG: found bracketed line: {}".format(line)) if debug else None
            line = line[1:-2] + "\n"

        # 6. If line starts with more than one single quote, remove all the single quotes at start
        match = re.match("""^'{2,}(.*)""", line)
        if match is not None:
            print("DEBUG: remove extraneous prefixed single quotes in line {}".format(line)) if debug\
                else None
            line = match.group(1)

        # 7. If line ends with more than one single quote, remove all the single quotes at start
        match = re.match("""(.*)'{2,}$""", line)
        if match is not None:
            print("DEBUG: remove extraneous suffixed single quotes in line {}".format(line)) if debug \
                else None
            line = match.group(1) + "\n"

        # 8. If line starts with just whitespace and/or asterisks, remove them
        match = re.match("""^[* ]+(.*)""", line)
        if match is not None:
            print("DEBUG: remove extraneous prefixed spaces/asterisks in line {}".format(line)) \
                if debug else None
            line = match.group(1)

        res_lines.append(line)

    with open(processed_list_file, 'w+') as f:
        f.writelines(res_lines)
