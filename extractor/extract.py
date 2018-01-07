import requests
import datetime
from ..util import config_parser

config = config_parser.parse_config()
api_key = config['api_key']

def download_today_xml_hansard():
    """
    Download today's Hansard if no date specified. There may not be a Hansard
    for today!
    """
    download_xml_hansard(datetime.datetime.today())

def download_xml_hansard(date: datetime.datetime, twfy_key: str = api_key):
    """
    Given a datetime date, download the Hansard xml for the specified date
    :param date: datetime date for the day of the debate
    :param twfy_key: API key
    :return:
    """
    datestring = "{}-{}-{}".format(date.year, date.month, date.day)
    resp = requests.get('https://www.theyworkforyou.com/api/getDebates?date={}&type=commons&key={}&output=xml'.format(datestring, twfy_key))
    return resp.text

def download_xml_debate(date: datetime, debate_id: str):
    resp = requests.get('https://www.theyworkforyou.com/pwdata/scrapedxml/debates/debates2017-12-04a.xml') # TODO make dynamic
    with open('hansard_{}_{}.xml'.format(date, debate_id, 'wb') as hansard_file:
        hansard_file.write(resp.content)
