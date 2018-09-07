from lxml import etree  # type: ignore
from typing import Generator
import glob
import os


def unxml_hansard_document(document_text):
    """
    Do preprocessing on a hansard doc expressed in text-xml. This includes html-unescaping and
    removing tags. It could change in future.
    :param document_text:
    :return:
    """
    # Declare that strings are Unicode-encoded
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    tree = etree.fromstring(document_text.encode('utf-8'), parser=parser)
    notags = etree.tostring(tree, encoding='utf8', method='text')
    return notags


def process_hansard_directory(dir_path):
    print("Processing Hansard directory {}".format(dir_path))
    for _file in glob.glob("{dir_path}/*.xml".format(dir_path=dir_path)):
        print("Found file {}".format(_file))
        process_hansard_file(_file)


def process_hansard_file(file_path):
    """
    file_path e.g. "hansard_gathering/raw_hansard_data/1919-02-04/MyDebate.xml"
    """
    print("Processing {}".format(file_path))
    dest_path = file_path.replace("raw_hansard_data", "processed_hansard_data").replace(".xml", ".txt")
    with open(file_path) as f:
        document_text = f.read()
        processed_document_text = unxml_hansard_document(document_text)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'wb+') as f:
        f.write(processed_document_text)


def list_raw_hansard_files() -> Generator[str, None, None]:
    for _file in glob.glob("hansard_gathering/raw_hansard_data/**/*.xml", recursive=True):
        yield _file


def process_all_hansard_files():
    for hansard_file in list_raw_hansard_files():
        process_hansard_file(hansard_file)
