from lxml import etree
from typing import List
import glob
import os


def unxml_hansard_document(document_text):
    """
    Do preprocessing on a hansard doc expressed in text-xml. This includes html-unescaping and
    removing tags. It could change in future.
    :param document_text:
    :return:
    """
    tree = etree.fromstring(document_text)
    notags = etree.tostring(tree, encoding='utf8', method='text')
    return notags


def interpolate_nes(document_text):
    pass


def process_hansard_file(file_path):
    """
    file_path e.g. "hansard_gathering/raw_hansard_data/1919-02-04/MyDebate.xml"
    """
    with open(file_path) as f:
        document_text = f.read()
        processed_document_text = unxml_hansard_document(document_text)
    dest_path = "hansard_gathering/processed_hansard_data/{}".format(file_path.replace(".xml", ".txt"))
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb+') as f:
        f.write(processed_document_text)


def list_hansard_files() -> List[str]:
    for _file in glob.glob("hansard_gathering/raw_hansard_data/**/*.xml", recursive=True):
        print("BLAH: {}".format(_file))
        yield _file


def process_all_hansard_files():
    for hansard_file in list_hansard_files():
        process_hansard_file(hansard_file)
