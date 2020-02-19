
import os

from blanket.exceptions import ParserIOError
from blanket.parser.base import parse_xml, parse_txt
from blanket.parser.gcov import GCovParser
from blanket.parser.llvm import LLVMParser
from blanket.utils import LLVM_HEADINGS


class ParserFactory(object):

    parsers = {
        "gcov": GCovParser,
        "llvm": LLVMParser
    }

    def __init__(self, path_handler, file_state_cache):
        self._path_handler = path_handler
        self._file_state_cache = file_state_cache

    def create_parser(self, content_xml_reference):
        directory, filename = os.path.split(content_xml_reference)
        data_filename = self._path_handler.resolve_path(directory, filename)
        self._file_state_cache.update(data_filename)
        try:
            root_node = parse_xml(data_filename)
            parser_type = _content_type(root_node)
        except ParserIOError:
            headings = parse_txt(data_filename)
            parser_type = _content_type(headings)

        if parser_type == "unknown":
            raise ParserIOError("Unknown coverage document", data_filename)

        return self.parsers[parser_type](data_filename)


def _content_type(content):
    if isinstance(content, list) and len(content) == 10:
        if content == LLVM_HEADINGS:
            return "llvm"
    elif hasattr(content, 'tagName') and content.tagName == "coverage":
        return "gcov"

    return "unknown"
