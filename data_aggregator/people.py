import csv

from util import capitalise_text, write_to_data_file

from typing import List


def main():
    nyc_baby_names = process_kaggle_nyc_baby_names()
    write_to_data_file(nyc_baby_names, "people", "nyc_baby_names.txt")


def process_kaggle_nyc_baby_names():
    with open('Most_Most_Popular_Baby_Names_by_Sex_and_Mother_s_Ethnic_Group__New_York_City.csv') as f:
        data = f.readlines()
        for row in csv.reader(data):
            yield capitalise_text(row[3])


def dbpedia_do_sparql_query(sparql_query: str):
    from SPARQLWrapper import SPARQLWrapper, JSON
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def dbpedia_sparql_get_people_count() -> int:
    sparql_query = """
    PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX  dbo: <http://dbpedia.org/ontology/>
    PREFIX  dbp: <http://dbpedia.org/property/>
    
    SELECT COUNT(*)
    WHERE{
        ?resource  rdf:type  dbo:Person.
    }
    """
    res = dbpedia_do_sparql_query(sparql_query)
    return int(res['results']['bindings'][0]['callret-0']['value'])


def dbpedia_sparql_search_people(people_list_file):
    # With help from https://rdflib.github.io/sparqlwrapper/
    # and https://stackoverflow.com/questions/38332857/
    # sparql-query-to-get-all-person-available-in-dbpedia-is-showing-only-some-person

    total_people = dbpedia_sparql_get_people_count()
    for i in range(0, total_people, 10000):
        people_list = []
        offset = str(i)
        print("We're at {sofar} out of {total}".format(sofar=offset,total=total_people))
        sparql_query = """
        PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX  dbo: <http://dbpedia.org/ontology/>
        PREFIX  dbp: <http://dbpedia.org/property/>
        SELECT ?resource
        WHERE { ?resource  rdf:type  dbo:Person.

        }
        ORDER BY ASC(?name) // TODO this doesn't work
        """
        sparql_query_offset = "LIMIT 10000 OFFSET {}".format(offset)
        response = dbpedia_do_sparql_query(sparql_query + sparql_query_offset)
        results = response['results']['bindings']
        people_list.extend([res['resource']['value'].split("/")[-1] for res in results])
        print("Adding {count} to people list file".format(count=len(results)))
        with open(people_list_file, 'w') as f:
            f.writelines("\n".join(people_list))

