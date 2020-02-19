
class ModifiedTimerError(Exception):
    pass


class BlanketError(Exception):
    pass


class ParserIOError(Exception):

    def __init__(self, error, filename):
        Exception.__init__(self, error)

        self._error = error
        self._filename = filename

    def __str__(self):
        return "file %s: %s" % (self._filename, self._error)


class RendererError(BlanketError):
    pass
