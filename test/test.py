from driver import driver
from driver.exception import SiblingNotFoundException

import lxml.etree as etree
import pytest


def test_has_sibling_correctly_returns_sibling():
    root = etree.Element("root")
    etree.SubElement(root, "child").text = "Child 1"
    etree.SubElement(root, "sister").text = "Child 2"
    assert driver.has_sibling(root, "sister") is False
    assert driver.has_sibling(root[0], "sister") is True


def test_get_sibling_returns_sibling_node_with_correct_tag():
    root = etree.Element("root")
    etree.SubElement(root, "child").text = "Child 1"
    etree.SubElement(root, "sister").text = "Child 2"
    etree.SubElement(root, "brother").text = "Child 3"
    assert driver.get_sibling(root[1], 'brother') == root[2]


def test_get_sibling_raises_exception():
    root = etree.Element("root")
    etree.SubElement(root, "child").text = "Child 1"
    etree.SubElement(root, "sister").text = "Child 2"
    etree.SubElement(root, "brother").text = "Child 3"
    with pytest.raises(SiblingNotFoundException):
        driver.get_sibling(root[1], 'mario')
