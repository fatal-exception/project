import csv
from typing import List

import util


def main():
    nyc_baby_names = sorted(set(process_kaggle_nyc_baby_names()))
    util.write_to_data_file(nyc_baby_names, "people", "nyc_baby_names.txt")


def process_kaggle_nyc_baby_names() -> List[str]:
    with open('raw_ne_data/Most_Popular_Baby_Names_by_Sex_and_Mother_s_Ethnic_Group__New_York_City.csv') as f:
        data = f.readlines()
        for row in csv.reader(data):
            yield row[3].capitalize()


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
    res = util.dbpedia_do_sparql_query(sparql_query)
    return int(res['results']['bindings'][0]['callret-0']['value'])


def dbpedia_sparql_search_people(people_list_file):
    # With help from https://rdflib.github.io/sparqlwrapper/
    # and https://stackoverflow.com/questions/38332857/
    # sparql-query-to-get-all-person-available-in-dbpedia-is-showing-only-some-person

    total_people = dbpedia_sparql_get_people_count()
    for i in range(0, total_people, 10000):
        people_list = []
        offset = str(i)
        print("We're at {sofar} out of {total}".format(sofar=offset, total=total_people))
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
        response = util.dbpedia_do_sparql_query(sparql_query + sparql_query_offset)
        results = response['results']['bindings']
        people_list.extend([res['resource']['value'].split("/")[-1] for res in results])
        print("Adding {count} to people list file".format(count=len(results)))
        with open(people_list_file, 'w') as f:
            f.writelines("\n".join(people_list))

