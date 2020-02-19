
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from blanket.exceptions import ParserIOError
from blanket.utils import LLVM_HEADINGS, LLVM_HEADINGS_RE


class Parser(object):

    def __init__(self):
        self._cache = {}
        self._data = None

    def data(self):
        return self._data

    def kind(self):
        return self._data["kind"]


def parse_xml(in_filename):
    try:
        doc = minidom.parse(in_filename)
    except IOError as e:
        raise ParserIOError(e, in_filename)
    except ExpatError as e:
        raise ParserIOError(e, in_filename)

    root_node = doc.documentElement

    return root_node


def parse_txt(in_filename):

    with open(in_filename) as f:
        for line in f:
            result = LLVM_HEADINGS_RE.match(line)
            if result:
                return LLVM_HEADINGS

    return []
