
from docutils.parsers.rst.directives import flag

from blanket.directive.base import BaseDirective


class CoverageDirective(BaseDirective):
    required_arguments = 1
    optional_arguments = 2
    option_spec = {
        "summary": flag,
        "full-report": flag,
    }
    has_content = True
    final_argument_whitespace = True

    def run(self):
        name = self.arguments[0]
        parser = self._parser_factory.create_parser(name)
        parser.build()

        renderer_type = "report"
        if "summary" in self.options:
            renderer_type = "summary"
        elif "full-report" in self.options:
            renderer_type = "full-report"

        renderer = self._renderer_factory.create_renderer(parser.kind(), renderer_type)

        return renderer.render(parser.data())


