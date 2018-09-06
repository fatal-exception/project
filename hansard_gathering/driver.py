from config_util.config_parser import parse_config
from datetime import datetime, timedelta
from urllib.parse import urlparse
from lxml import etree  # type: ignore
import concurrent.futures
import json
import lxml  # type: ignore
import os
import requests
import re
import sys

# Prefixes used for each content type by TWFY
# 'Content-Type': ['url-prefix', 'file-prefix']
prefixes = {'Wrans': ['wrans', 'answers'],
            'WMS': ['wms', 'ministerial'],
            'Debates': ['debates', 'debates']}


def get_debate_colnum_start(debate) -> int:
    return int(urlparse(debate[1]).query.split(".")[1])


def get_debate_colnum_end(idx, debates_list) -> int:
    if idx == len(debates_list) - 1:
        # This is last debate in xml, so get all remaining columns
        return sys.maxsize
    else:
        # My last colnum is the colnum at which next debate starts
        return get_debate_colnum_start(debates_list[idx + 1])


def remove_other_debate_content(tree, debate_colnum_start, debate_colnum_end):
    elem_types = "speech major-heading minor-heading oral-heading".split()
    for elem_type in elem_types:
        for tag in tree.findall(elem_type):
            colnum = tag.attrib['colnum']
            if int(colnum) not in range(debate_colnum_start, debate_colnum_end):
                tree.remove(tag)
    return tree


def download_and_split_all_debates(datestring, debates_list):
    """
    Given a list of debate titles, download them all into files,
    correctly splitting the XML into separate files per title.
    :param datestring: Date to download for
    :param debates_list: List of tuples of (title, HTML url, XML url)
    """
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    for idx, debate in enumerate(debates_list):
        print("Data for {}: {}".format(datestring, debate))
        xml_url = debate[2]
        if xml_url == "N/A":
            continue
        title = debate[0].replace("/", "")  # UNIX filenames cannot contain forward slash
        debate_colnum_start: int = get_debate_colnum_start(debate)
        debate_colnum_end: int = get_debate_colnum_end(idx, debates_list)

        xml_data = requests.get(xml_url).text
        tree = etree.fromstring(xml_data.encode('utf-8'), parser=parser)

        tree = remove_other_debate_content(tree, debate_colnum_start, debate_colnum_end)

        os.makedirs("hansard_gathering/raw_hansard_data/{datestring}".format(datestring=datestring), exist_ok=True)
        with open("hansard_gathering/raw_hansard_data/{datestring}/{title}.xml".format(
                datestring=datestring, title=title), "w") as f:
            f.write(lxml.etree.tostring(tree).decode('utf-8'))


def download_all_debates(datestring, debates_list):
    """
    Given a list of debate titles, download all of them into files.
    """
    for debate in debates_list:
        print("Data for {}: {}".format(datestring, debate))
        title = debate[0].replace("/", "")  # UNIX filenames cannot contain forward slash
        xml_url = debate[2]
        if xml_url == "N/A":
            continue
        xml_data = requests.get(xml_url).text
        os.makedirs("hansard_gathering/raw_hansard_data/{datestring}".format(datestring=datestring), exist_ok=True)
        with open("hansard_gathering/raw_hansard_data/{datestring}/{title}.xml".format(
                datestring=datestring, title=title), "w") as f:
            f.write(xml_data)


def get_titles_and_download(datestring, content_type):
    commons_titles = get_hansard_titles(datestring, content_type, "commons")

    # TODO lords titles don't seem to work with scraped xml?
    lords_titles = get_hansard_titles(datestring, "Debates", "lords")

    download_and_split_all_debates(datestring, commons_titles)


def get_hansards_for_date(date):
    date_regex = re.compile(r"\d\d\d\d-\d\d-\d\d")
    assert date_regex.match(date), \
        "Date must be yyyy-mm-dd"

    get_titles_and_download(date, "Debates")


def get_all_hansards(start_year=1919, start_month=1, start_day=1):
    """
    Generate all datestrings from now back to March 29, 1803 (when Hansard started).
    Get all available debates for each.
    """
    def date_gen():
        year = start_year
        month = start_month
        day = start_day
        now_dt = datetime.now()
        then_dt = datetime(year, month, day)

        # While it's less than today
        while then_dt < now_dt:
            _datestring = "{}-{}-{}".format(
                str(then_dt.year),
                str(then_dt.month).zfill(2),
                str(then_dt.day).zfill(2))

            yield _datestring
            then_dt += timedelta(days=1)

    dg = date_gen()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for datestring in dg:
            executor.submit(get_titles_and_download, datestring, "Debates")


def get_hansard_titles(datestring, content_type, house="commons"):
    """
    Given a date, download the Hansard xml of specified content for the specified date
    :param datestring: e.g. '2017-12-04'
    :param content_type: Wrans, WMS or Debates
    :param house: commons or lords
    :return List of titles extracted from the json, as well as their HTML and XML urls
    """
    twfy_key = parse_config()['api_key']

    request_url = 'https://www.theyworkforyou.com/api/get{}?date={}&key={}&output=json'\
        .format(content_type, datestring, twfy_key)

    if content_type == 'Debates':
        request_url += '&type={}'.format(house)

    resp = requests.get(request_url)

    resp_data = json.loads(resp.text)
    if type(resp_data) == dict and resp_data.get("error", "") == "No data to display":
        return [("No data to display for this date", "N/A", "N/A")]
    else:

        titles = []
        for elem in resp_data:
            entry = elem["entry"]  # my dear Watson
            if "listurl" in entry and "body" in entry:
                titles.append((entry["body"], make_twfy_html_url(entry["listurl"]),
                               make_twfy_xml_url(entry["listurl"], content_type)))
        return titles


def make_twfy_html_url(text):
    return 'https://www.theyworkforyou.com{}'.format(text)


def make_twfy_xml_url(text, content_type):

    return 'https://www.theyworkforyou.com/pwdata/scrapedxml/{}/{}{}.xml' \
        .format(prefixes[content_type][0],
                prefixes[content_type][1],
                text.split('=')[1].split('.')[0])
