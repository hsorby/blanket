
from blanket.renderer.report import ReportRenderer
from blanket.renderer.summary import SummaryRenderer


class RendererFactory(object):

    renderers = {
        "summary": SummaryRenderer,
        "report": ReportRenderer,
    }

    def create_renderer(self, kind, option):
        return self.renderers[option](kind)
