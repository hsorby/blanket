
import re

from docutils import nodes

from blanket.exceptions import RendererError
from blanket.renderer.base import BaseRenderer


class ReportRenderer(BaseRenderer):

    def render(self, data):
        if self._kind == "gcov":
            return _render_gcov(data)
        elif self._kind == "llvm":
            return _render_llvm(data)
        else:
            raise RendererError("Unknown data type '{0}'".format(self._kind))


def _render_llvm(data):
    column_widths = (3, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    section_id = "fjlijf38u309098"
    section = nodes.section(ids=["{0}".format(section_id)])
    section += nodes.title(text="LLVM Code Coverage Report")
    table = nodes.table()

    table_data = data["table-data"]
    headings = table_data.pop(0)

    table_group = nodes.tgroup(cols=len(headings))
    table += table_group
    for column_width in column_widths:
        table_group += nodes.colspec(colwidth=column_width)

    table_head = nodes.thead()
    table_group += table_head
    table_head += _create_table_row(headings)

    table_body = nodes.tbody()
    table_group += table_body
    for data_row in table_data:
        table_body += _create_table_row(data_row)

    section += table

    return [section]


def _render_gcov(data):
    line_data = _convert_to_line_data(data)
    lines_covered = data["summary"]["lines-covered"]
    lines_total = data["summary"]["lines-valid"]
    lines_percentage = float(data["summary"]["line-rate"])

    line_data.append(["Total", lines_total, lines_covered, "{0:.0%}".format(lines_percentage), ""])

    headings = ["File", "Lines", "Exec", "Cover", "Missing"]
    column_widths = (3, 1, 1, 1, 1)

    section_id = "88j8jd38jr38erj3"  # hash(frozenset(data.items()))
    section = nodes.section(ids=["{0}".format(section_id)])
    section += nodes.title(text="GCC Code Coverage Report")
    table = nodes.table()

    table_group = nodes.tgroup(cols=len(headings))
    table += table_group
    for column_width in column_widths:
        table_group += nodes.colspec(colwidth=column_width)

    table_head = nodes.thead()
    table_group += table_head
    table_head += _create_table_row(headings)

    table_body = nodes.tbody()
    table_group += table_body
    for data_row in line_data:
        table_body += _create_table_row(data_row)

    section += table

    return [section]


def _create_table_row(row_cells):
    row = nodes.row()
    for cell in row_cells:
        entry = nodes.entry()
        row += entry
        entry += nodes.paragraph(text=cell)
    return row


def _convert_to_line_data(data_in):
    data_out = []
    for package in data_in["packages"]:
        for class_ in package["classes"]:
            percentage = "{0:.0%}".format(float(class_["line-rate"]))
            missing = ', '.join(class_["lines-missed"])
            data_out.append([class_["filename"], class_["lines-valid"], class_["lines-executed"], percentage, missing])

    return data_out


def remove_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)
