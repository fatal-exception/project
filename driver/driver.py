from util.config_parser import parse_config
from exception import SiblingNotFoundException
import requests
import lxml.etree as etree


def get_hansard_debate_titles(datestring):
    twfy_key = parse_config()["api_key"]
    resp = requests.get(
        'https://www.theyworkforyou.com/api/getDebates?date={}&type=commons&key={}&output=xml'
        .format(datestring, twfy_key))
    root = etree.fromstring(resp.content)
    titles = []
    for elem in root.iter():
        if elem.tag == 'body' and has_sibling(elem, 'listurl'):
            listurl_elem = get_sibling(elem, 'listurl')
            titles.append((elem.text, make_twfy_debate_html_url(listurl_elem.text),
                           make_twfy_debate_xml_url(listurl_elem.text)))
    return titles


def get_hansard_wms_titles(datestring):
    """
    Given a datetime date, download the Hansard xml for the specified date
    :param datestring: e.g. '2017-12-04'
    :return xml in a unicode string, of the hansard list of debates from TWFY
    """
    twfy_key = parse_config()["api_key"]
    resp = requests.get('https://www.theyworkforyou.com/api/getWMS?date={}&key={}&output=xml'
                        .format(datestring, twfy_key))

    xml_root = etree.fromstring(resp.content)

    titles = []
    for elem in xml_root.iter():
        if elem.tag == 'body' and has_sibling(elem, 'listurl'):
            listurl_elem = get_sibling(elem, 'listurl')
            titles.append((elem.text, make_twfy_wms_html_url(listurl_elem.text), make_twfy_wms_xml_url(listurl_elem.text)))

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


def make_twfy_debate_html_url(text):
    return 'https://www.theyworkforyou.com{}'.format(text)


def make_twfy_debate_xml_url(text):
    return 'https://www.theyworkforyou.com/pwdata/scrapedxml/debates/debates{}.xml'\
        .format(text.split('=')[1].split('.')[0])


def make_twfy_wms_html_url(text):
    return 'https://www.theyworkforyou.com{}'.format(text)


def make_twfy_wms_xml_url(text):
    return 'https://www.theyworkforyou.com/pwdata/scrapedxml/wms/ministerial{}.xml' \
        .format(text.split('=')[1].split('.')[0])
