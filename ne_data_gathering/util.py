from typing import List
from os.path import realpath, dirname

import os

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
