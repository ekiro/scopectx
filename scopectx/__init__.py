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
        frame_hash = hash(frame)
        if frame_hash in self.frames_data:
            raise DuplicateContextException
        self.frames_data[frame_hash] = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        frame = inspect.currentframe().f_back
        del self.frames_data[hash(frame)]

    def _find_context_frame(self):
        frame = inspect.currentframe().f_back

        while frame:
            frame_hash = hash(frame)
            if frame_hash in self.frames_data:
                return frame_hash

            frame = frame.f_back

        raise NotInContextException

    def __getitem__(self, item):
        frame_hash = self._find_context_frame()
        data = self.frames_data[frame_hash]
        return data[item]

    def __setitem__(self, key, value):
        frame_hash = self._find_context_frame()
        data = self.frames_data[frame_hash]
        data[key] = value


class MultiLevelContext(Context):
    def _iter_context_frames(self):
        frame = inspect.currentframe().f_back

        while frame:
            frame_hash = hash(frame)
            if frame_hash in self.frames_data:
                yield frame_hash
            frame = frame.f_back

    def __getitem__(self, item):
        frame_iterator = self._iter_context_frames()
        try:
            frame_hash = next(frame_iterator)
        except StopIteration:
            raise NotInContextException

        while frame_hash:
            data = self.frames_data[frame_hash]
            if item in data:
                return data[item]
            else:
                frame_hash = next(frame_iterator, None)

        raise KeyError(item)
