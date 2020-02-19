
import os
import re

from blanket.exceptions import ModifiedTimerError

LLVM_HEADINGS = ["Filename", "Regions", "Missed Regions", "Cover", "Functions",
                 "Missed Functions", "Executed", "Lines", "Missed Lines", "Cover"]

LLVM_HEADINGS_RE = re.compile(r"(Filename)\s+(Regions)\s+(Missed Regions)\s+(Cover)\s+(Functions)\s+(Missed Functions)"
                              r"\s+(Executed)\s+(Lines)\s+(Missed Lines)\s+(Cover)")


class PathHandler(object):

    def __init__(self, config_directory):

        self._config_directory = config_directory

    def resolve_path(self, directory, filename):
        """Returns a full path to the filename in the given directory assuming that if the directory
        path is relative, then it is relative to the conf.py directory.
        """

        if os.path.isabs(directory):
            return os.path.join(directory, filename)

        return os.path.join(self._config_directory, directory, filename)


class ModifiedTimer(object):

    def __init__(self, getmtime):
        self._getmtime = getmtime

    def get_modified_time(self, filename):

        try:
            return self._getmtime(filename)
        except OSError:
            raise ModifiedTimerError('Cannot find file: %s' % os.path.realpath(filename))


class FileStateCache(object):
    """
    Stores the modified time of the various coverage xml files against the
    reStructuredText file that they are referenced from so that we know which
    reStructuredText files to rebuild if the coverage xml is modified.

    We store the information in the environment object so that it is pickled
    down and stored between builds as Sphinx is designed to do.
    """

    def __init__(self, modified_timer, app):

        self.app = app
        self._modified_timer = modified_timer

    def update(self, source_file):

        if not hasattr(self.app.env, "blanket_file_state"):
            self.app.env.blanket_file_state = {}

        new_modified_time = self._modified_timer.get_modified_time(source_file)

        modified_time, doc_names = self.app.env.blanket_file_state.setdefault(
            source_file, (new_modified_time, set())
            )

        doc_names.add(self.app.env.docname)

        self.app.env.blanket_file_state[source_file] = (new_modified_time, doc_names)

    def get_outdated(self, app, env, added, changed, removed):

        if not hasattr(self.app.env, "blanket_file_state"):
            return []

        stale = []

        for filename, info in self.app.env.blanket_file_state.items():
            old_modified_time, doc_names = info
            if self._modified_timer.get_modified_time(filename) > old_modified_time:
                stale.extend(doc_names)

        return list(set(stale).difference(removed))

    def purge_doc(self, app, env, doc_name):

        if not hasattr(self.app.env, "blanket_file_state"):
            return

        to_remove = []

        for filename, info in self.app.env.blanket_file_state.items():

            _, doc_names = info
            doc_names.discard(doc_name)
            if not doc_names:
                to_remove.append(filename)

        for filename in to_remove:
            del self.app.env.blanket_file_state[filename]
