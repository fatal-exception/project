#!/usr/bin/env python

from ftplib import FTP
from os.path import realpath, dirname
from typing import List
from util import capitalise_text, write_to_data_file

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


def process_lse_download() -> List[str]:
    # manually downloaded on 3rd March 2018 from
    # http://www.londonstockexchange.com/statistics/companies-and-issuers/companies-defined-by-mifir-identifiers-list-on-lse.xlsx
    # Pandas cannot cope with this xlsx :(
    with open('lse_manual_download.txt') as f:
        lse = f.readlines()

    return capitalise_text(lse)


def main() -> None:
    # FTP companies data is too dirty to use :(

    nasdaq_csv_companies = dedup(process_nasdaq_csv())
    write_to_data_file(nasdaq_csv_companies, "companies" "nasdaq_csv_companies.txt")

    lse = process_lse_download()
    write_to_data_file(lse, "companies", "lse_manual_download.txt")


if __name__ == "__main__":
    main()