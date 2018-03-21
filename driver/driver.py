from util.config_parser import parse_config
from driver.exception import SiblingNotFoundException
import requests
import lxml.etree as etree

# Prefixes used for each content type by TWFY
# 'Content-Type': ['url-prefix', 'file-prefix']
prefixes = {'Wrans': ['wrans', 'answers'],
            'WMS': ['wms', 'ministerial'],
            'Debates': ['debates', 'debates']}


def get_hansard_titles(datestring, content_type):
    """
    Given a date, download the Hansard xml of specified content for the specified date
    :param datestring: e.g. '2017-12-04'
    :param content_type: Wrans, WMS or Debates
    :return List of titles extracted from the json, as well as their HTML and XML urls
    """
    twfy_key = parse_config()['api_key']

    request_url = 'https://www.theyworkforyou.com/api/get{}?date={}&key={}&output=xml'\
        .format(content_type, datestring, twfy_key)

    if content_type == 'Debates':
        request_url += '&type=commons'

    resp = requests.get(request_url)

    if "No data to display" in resp.text:
        return [("No data to display for this date", "N/A", "N/A")]
    else:

        xml_root = etree.fromstring(resp.content)

        titles = []
        for elem in xml_root.iter():
            if elem.tag == 'body' and has_sibling(elem, 'listurl'):
                listurl_elem = get_sibling(elem, 'listurl')
                titles.append((elem.text, make_twfy_html_url(listurl_elem.text),
                               make_twfy_xml_url(listurl_elem.text, content_type)))

        return titles


def has_sibling(elem, tag_name):
    """
    return True if the given LXML Etree Element has a sibling with the given tag:
    :param elem: Element being examined
    :param tag_name:
    :return: True if the elem has >= 1 signling with tag_name
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
    :return: True if the elem has >= 1 signling with tag_name
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

