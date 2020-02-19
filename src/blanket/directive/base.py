
from abc import ABC

from docutils.parsers import rst


class BaseDirective(rst.Directive, ABC):

    def __init__(self, project_info_factory, parser_factory, renderer_factory, *args):
        rst.Directive.__init__(self, *args)
        self._project_info_factory = project_info_factory
        self._parser_factory = parser_factory
        self._renderer_factory = renderer_factory
        self._directive_args = list(args)  # Convert tuple to list to allow modification.
