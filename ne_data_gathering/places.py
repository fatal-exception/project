#!/usr/bin/env python
import os
import sys
import util


def dbpedia(src_dir, file_path):
    dbpedia_sparql_extract_places("{}{}".format(src_dir, file_path))
    util.dbpedia_post_processing(
        "{}{}".format("raw_ne_data", file_path), "{}{}".format("processed_ne_data", file_path))


def conll2003eng():
    conll_places = util.process_conll_file(util.conll_file, 'LOC')
    util.write_to_data_file(conll_places, "places", "conll_2003.txt")


def main(src_dir, file_path) -> None:

    dbpedia(src_dir, file_path)
    conll2003eng()


def dbpedia_sparql_get_place_count() -> int:
    sparql_query = """
    PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX  dbo: <http://dbpedia.org/ontology/>
    PREFIX  dbp: <http://dbpedia.org/property/>

    SELECT COUNT(*)
    WHERE { ?resource  foaf:name ?name .
            ?resource  rdf:type  dbo:Place .
    }
    """
    res = util.dbpedia_do_sparql_query(sparql_query)
    return int(res['results']['bindings'][0]['callret-0']['value'])


def dbpedia_sparql_extract_places(list_file):
    # With help from https://rdflib.github.io/sparqlwrapper/
    # and https://stackoverflow.com/questions/38332857/

    if os.path.exists(list_file):
        os.unlink(list_file)
    total = dbpedia_sparql_get_place_count()
    for i in range(0, total, 10_000):
        result_list = []
        offset = str(i)
        print("We're at {sofar} out of {total}".format(sofar=offset, total=total))
        sparql_query = """
        PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX  dbo: <http://dbpedia.org/ontology/>
        PREFIX  dbp: <http://dbpedia.org/property/>
        SELECT ?name
        WHERE { ?resource  foaf:name ?name .
                ?resource  rdf:type  dbo:Place .
        }
        """
        sparql_query_offset = "LIMIT 10000 OFFSET {}".format(offset)
        response = util.dbpedia_do_sparql_query(sparql_query + sparql_query_offset)
        results = response['results']['bindings']
        result_list.extend([res['name']['value'] for res in results])
        print("Adding {count} to places list file".format(count=len(results)))
        with open(list_file, 'a') as f:
            f.writelines("\n".join(result_list))


if __name__ == "__main__":
    global_file_path = "/places/dbpedia.txt"
    global_src_dir = "raw_ne_data"
    if sys.argv[1] == "main":
        main(global_src_dir, global_file_path)
    elif sys.argv[1] == "process":
        util.dbpedia_post_processing(
            "{}{}".format("raw_ne_data", global_file_path), "{}{}".format(
                "processed_ne_data", global_file_path))
