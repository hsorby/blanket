
from docutils import nodes

from blanket.exceptions import RendererError
from blanket.renderer.base import BaseRenderer


class SummaryRenderer(BaseRenderer):

    def render(self, data):
        if self._kind == "gcov":
            return _render_gcov(data["summary"])
        elif self._kind == "llvm":
            return _render_llvm(data["summary"])
        else:
            raise RendererError("Unknown data type '{0}'".format(self._kind))


def _render_gcov(data):
    lines_covered = data["lines-covered"]
    lines_total = data["lines-valid"]
    lines_percentage = float(data["line-rate"])
    lines_summary = "Used {0} line{1} out of {2} for {3:.0%} line coverage." \
        .format(lines_covered, "s" if int(lines_covered) > 1 else "", lines_total, lines_percentage)

    branches_covered = data["branches-covered"]
    branches_total = data["branches-valid"]
    branches_percentage = float(data["branch-rate"])
    branches_summary = "Executed {0} branche{1} out of {2} for {3:.0%} branch coverage." \
        .format(branches_covered, "s" if int(branches_covered) > 1 else "", branches_total, branches_percentage)

    section_id = "blanket_gcov_summary_heading"
    section = nodes.section(ids=["{0}".format(section_id)])
    section += nodes.title(text="Coverage Summary")
    section += nodes.paragraph(text=lines_summary)
    section += nodes.paragraph(text=branches_summary)

    return [section]


def _render_llvm(data):
    section_id = "blanket_llvm_summary_heading"
    section = nodes.section(ids=["{0}".format(section_id)])
    section += nodes.title(text="Coverage Summary")

    lines_total = data[7]
    lines_missed = data[8]
    lines_percentage = data[9]
    lines_summary = "Missed {0} line{1} out of {2} for {3} line coverage." \
        .format(lines_missed, "" if int(lines_missed) == 1 else "s", lines_total, lines_percentage)
    section += nodes.paragraph(text=lines_summary)

    return [section]
