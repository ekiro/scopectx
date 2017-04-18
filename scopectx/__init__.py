import inspect


class NotInContextException(Exception):
    pass


class DuplicateContextException(Exception):
    pass


class Context(object):
    def __init__(self):
        self.frames_data = {}

    def __enter__(self):
        frame = inspect.currentframe().f_back
        if frame in self.frames_data:
            raise DuplicateContextException
        self.frames_data[frame] = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        frame = inspect.currentframe().f_back
        del self.frames_data[frame]

    def _find_context_frame(self):
        frame = inspect.currentframe().f_back

        while frame:
            if frame in self.frames_data:
                return frame
            frame = frame.f_back

        raise NotInContextException

    def __getitem__(self, item):
        frame = self._find_context_frame()
        data = self.frames_data[frame]
        return data[item]

    def __setitem__(self, key, value):
        frame = self._find_context_frame()
        data = self.frames_data[frame]
        data[key] = value