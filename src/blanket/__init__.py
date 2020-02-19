__version__ = "0.1.0"


def setup(app):

    from . import directives

    directives.setup(app)
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
