
import os
import fnmatch

from blanket.directive.coverage import CoverageDirective
from blanket.parser.factory import ParserFactory
from blanket.renderer.factory import RendererFactory
from blanket.utils import PathHandler, ModifiedTimer, FileStateCache


class DirectiveContainer(object):

    def __init__(self, directive, *args):

        self._directive = directive
        self._args = args

        # Required for sphinx to inspect
        self.required_arguments = directive.required_arguments
        self.optional_arguments = directive.optional_arguments
        self.option_spec = directive.option_spec
        self.has_content = directive.has_content
        self.final_argument_whitespace = directive.final_argument_whitespace

    def __call__(self, *args):

        call_args = []
        call_args.extend(self._args)
        call_args.extend(args)

        return self._directive(*call_args)


class ProjectInfoFactory(object):

    def __init__(self, source_dir, build_dir, config_dir, match):

        self._source_dir = source_dir
        self._build_dir = build_dir
        self._config_dir = config_dir
        self._match = match

        self._projects = {}
        self._default_project = None

    def update(self, projects, default_project):
        self._projects = projects
        self._default_project = default_project


class CoverageDirectiveFactory(object):

    directives = {
        "coverage": CoverageDirective,
    }

    def __init__(self, project_info_factory, parser_factory, renderer_factory):
        self._project_info_factory = project_info_factory
        self._parser_factory = parser_factory
        self._renderer_factory = renderer_factory

    def create_directive_container(self, type_):

        return DirectiveContainer(
            self.directives[type_],
            self._project_info_factory,
            self._parser_factory,
            self._renderer_factory
        )

    def get_config_values(self, app):

        # All DirectiveContainers maintain references to this project info factory
        # so we can update this to update them
        self._project_info_factory.update(
            app.config.blanket_projects,
            app.config.blanket_default_project,
            )


def setup(app):

    path_handler = PathHandler(app.confdir)

    timer = ModifiedTimer(os.path.getmtime)
    file_state_cache = FileStateCache(timer, app)

    parser_factory = ParserFactory(path_handler, file_state_cache)
    renderer_factory = RendererFactory()

    build_dir = os.path.dirname(app.doctreedir.rstrip(os.sep))
    project_info_factory = ProjectInfoFactory(app.srcdir, build_dir, app.confdir, fnmatch.fnmatch)

    directive_factory = CoverageDirectiveFactory(project_info_factory, parser_factory, renderer_factory)

    def add_directive(name):
        app.add_directive(name, directive_factory.create_directive_container(name))

    add_directive('coverage')

    app.add_config_value("blanket_projects", {}, True)
    app.add_config_value("blanket_default_project", "", True)

    app.connect("builder-inited", directive_factory.get_config_values)

    app.connect("env-get-outdated", file_state_cache.get_outdated)

    app.connect("env-purge-doc", file_state_cache.purge_doc)
