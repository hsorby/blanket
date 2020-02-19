
from blanket.parser.base import Parser
from blanket.renderer.report import remove_ansi
from blanket.utils import LLVM_HEADINGS_RE, LLVM_HEADINGS


class LLVMParser(Parser):
    def __init__(self, filename):
        Parser.__init__(self)
        self._filename = filename

    def build(self):
        content = parse(self._filename)
        self._data = {"kind": "llvm", "summary": content[-1], "table-data": content}


def parse(filename):

    content = []
    table_start_found = False
    table_end_found = False
    with open(filename) as f:
        for line in f:
            if table_start_found and not table_end_found:
                line = line.rstrip()
                line = remove_ansi(line)
                parts = line.split(" ")
                parts = [x for x in parts if x]
                if len(parts) == 10:
                    content.append(parts)
                    if parts[0] == "TOTAL":
                        table_end_found = True
            elif not table_start_found:
                result = LLVM_HEADINGS_RE.match(line)
                if result:
                    table_start_found = True
                    content.append(LLVM_HEADINGS)

    return content
