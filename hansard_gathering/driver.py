from config_util.config_parser import parse_config
from datetime import datetime, timedelta
from hansard_gathering.exception import SiblingNotFoundException
import concurrent.futures
import json
import os
import requests

# Prefixes used for each content type by TWFY
# 'Content-Type': ['url-prefix', 'file-prefix']
prefixes = {'Wrans': ['wrans', 'answers'],
            'WMS': ['wms', 'ministerial'],
            'Debates': ['debates', 'debates']}


def download_all_debates(datestring, debates_list):
    """
    Given a list of debate titles, download all of them into files.
    """
    for debate in debates_list:
        print("Data for {}: {}".format(datestring, debate))
        title = debate[0]
        xml_url = debate[2]
        if xml_url == "N/A":
            continue
        xml_data = requests.get(xml_url).text
        os.makedirs("hansard_gathering/raw_hansard_data/{datestring}".format(datestring=datestring))
        with open("hansard_gathering/raw_hansard_data/{datestring}/{title}.xml".format(
                datestring=datestring, title=title), "w") as f:
            f.write(xml_data)


def get_titles_and_download(datestring, content_type):
    commons_titles = get_hansard_titles(datestring, content_type, "commons")
    lords_titles = get_hansard_titles(datestring, "Debates", "lords")
    download_all_debates(datestring, commons_titles)
    download_all_debates(datestring, lords_titles)


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
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
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


def has_sibling(elem, tag_name):
    """
    return True if the given LXML Etree Element has a sibling with the given tag:
    :param elem: Element being examined
    :param tag_name:
    :return: True if the elem has >= 1 sibling with tag_name
    """
    for sibling in elem.itersiblings():
        if sibling.tag == tag_name:
            return True
    return False


def get_sibling(elem, tag_name):
    """
    return True if the given LXML Etree Element has a sibling with the given tag:
    :param elem: Element being examined
    :param tag_name:
    :return: True if the elem has >= 1 sibling with tag_name
    """
    for sibling in elem.itersiblings():
        if sibling.tag == tag_name:
            return sibling
    raise SiblingNotFoundException


def make_twfy_html_url(text):
    return 'https://www.theyworkforyou.com{}'.format(text)


def make_twfy_xml_url(text, content_type):

    return 'https://www.theyworkforyou.com/pwdata/scrapedxml/{}/{}{}.xml' \
        .format(prefixes[content_type][0],
                prefixes[content_type][1],
                text.split('=')[1].split('.')[0])
