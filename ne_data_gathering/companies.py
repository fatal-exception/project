#!/usr/bin/env python

from ftplib import FTP
from typing import List
from util import capitalise_text_list, write_to_data_file
import util
import os

import csv
import requests


def download_nasdaq(data_files: List[str]) -> List[str]:
    class Reader:
        def __init__(self):
            self.data = ""

        def __call__(self, bytes_data):
            self.data += bytes_data.decode('utf-8')

    conn = FTP('ftp.nasdaqtrader.com')
    conn.login()
    conn.cwd('SymbolDirectory')
    r = Reader()
    for f in data_files:
        conn.retrbinary("RETR {}".format(f), r)

    return r.data.split("\n")


def filter_names(company_data: List[str]) -> List[str]:
    company_names = [d.split("|")[1] for d in company_data if len(d.split("|")) > 1]
    return list(filter(lambda company_name: company_name != "", company_names))


def process_nasdaq_ftp():
    data_files = ["nasdaqlisted.txt", "otherlisted.txt"]
    company_data = download_nasdaq(data_files)
    write_to_data_file(filter_names(company_data), "companies", "nasdaq_ftp_companies.txt")


def dedup(data: List[str]) -> List[str]:
    return list(set(data))


def process_nasdaq_csv() -> List[str]:
    nasdaq_exchanges = "AMEX NASDAQ NYSE".split()
    for exchange in nasdaq_exchanges:
        csv_url = "https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange={}&render=download"\
            .format(exchange)
        r = requests.get(csv_url)

        processed_text = r.text.replace("\r\n", "\n").replace("&#39;", "'")
        csv_data = processed_text.split("\n")
        reader = csv.reader(csv_data)
        for row in reader:
            if len(row) > 1:
                yield(row[1])


def dbpedia_sparql_get_company_count() -> int:
    sparql_query = """
    PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX  dbo: <http://dbpedia.org/ontology/>
    PREFIX  dbp: <http://dbpedia.org/property/>

    SELECT COUNT(*)
    WHERE { ?resource  foaf:name ?name .
            ?resource  rdf:type  dbo:Organisation .
    }
    """
    res = util.dbpedia_do_sparql_query(sparql_query)
    return int(res['results']['bindings'][0]['callret-0']['value'])


def dbpedia_sparql_extract_companies(company_list_file):
    # With help from https://rdflib.github.io/sparqlwrapper/
    # and https://stackoverflow.com/questions/38332857/
    # sparql-query-to-get-all-person-available-in-dbpedia-is-showing-only-some-person

    if os.path.exists(company_list_file):
        os.unlink(company_list_file)
    total = dbpedia_sparql_get_company_count()
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
                ?resource  rdf:type  dbo:Organisation .
        }
        """
        sparql_query_offset = "LIMIT 10000 OFFSET {}".format(offset)
        response = util.dbpedia_do_sparql_query(sparql_query + sparql_query_offset)
        results = response['results']['bindings']
        result_list.extend([res['name']['value'] for res in results])
        print("Adding {count} to companies list file".format(count=len(results)))
        with open(company_list_file, 'a') as f:
            f.writelines("\n".join(result_list))


def process_lse_download() -> List[str]:
    # manually downloaded on 3rd March 2018 from
    # http://www.londonstockexchange.com/statistics/companies-and-issuers/companies-defined-by-mifir-identifiers-list-on-lse.xlsx
    # Pandas cannot cope with this xlsx :(
    with open('raw_ne_data/lse_manual_download.txt') as f:
        lse = f.readlines()

    return capitalise_text_list(lse)


def main() -> None:
    # FTP companies data is too dirty to use :(

    nasdaq_csv_companies = dedup(process_nasdaq_csv())
    write_to_data_file(nasdaq_csv_companies, "companies", "nasdaq_csv_companies.txt")

    lse = process_lse_download()
    write_to_data_file(lse, "companies", "lse_manual_download.txt")

    dbpedia_sparql_extract_companies('processed_ne_data/companies/dbpedia.txt')

    def conll2003eng():
        conll_companies = util.process_conll_file(util.conll_file, 'ORG')
        util.write_to_data_file(conll_companies, "companies", "conll_2003.txt")

    conll2003eng()


if __name__ == "__main__":
    main()
