
from blanket.parser.base import Parser, parse_xml


class GCovParser(Parser):
    def __init__(self, filename):
        Parser.__init__(self)
        self._filename = filename

    def build(self):
        root_node = parse_xml(self._filename)
        self._data = _handle_coverage(root_node)


def _handle_coverage(node):
    summary = dict(node.attributes.items())
    coverage = {"kind": "gcov", "summary": summary}
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "sources":
                coverage["sources"] = _handle_sources(child)
            elif child.tagName == "packages":
                coverage["packages"] = _handle_packages(child)

    return coverage


def _handle_sources(node):
    sources = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "source":
                sources.append(_handle_source(child))

    return sources


def _handle_source(node):
    return node.firstChild.data


def _handle_packages(node):
    packages = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "package":
                packages.append(_handle_package(child))

    return packages


def _handle_package(node):
    package = {"classes": None}
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "classes":
                package["classes"] = _handle_classes(child)

    return package


def _handle_classes(node):
    classes = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "class":
                classes.append(_handle_class(child))

    return classes


def _handle_class(node):
    class_summary = dict(node.attributes.items())
    lines_valid = 0
    lines_executed = 0
    lines_missed = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "lines":
                class_lines = _handle_lines(child)
                lines_valid += class_lines[0]
                lines_executed += class_lines[1]
                lines_missed.extend(class_lines[2])
            elif child.tagName == "methods":
                method_lines = _handle_lines(child)
                lines_valid += method_lines[0]
                lines_executed += method_lines[1]
                lines_missed.extend(method_lines[2])

    class_summary["lines-valid"] = lines_valid
    class_summary["lines-executed"] = lines_executed
    class_summary["lines-missed"] = lines_missed

    return class_summary


def _handle_lines(node):
    return _do_line(node)


def _handle_methods(node):
    return _do_line(node)


def _do_line(node):
    lines_valid = 0
    lines_executed = 0
    lines_missed = []
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if child.tagName == "line":
                lines_valid += 1
                line = _handle_line(child)
                if int(line["hits"]) > 0:
                    lines_executed += 1
                else:
                    lines_missed.append(line["number"])

    return lines_valid, lines_executed, lines_missed


def _handle_line(node):
    return dict(node.attributes.items())
