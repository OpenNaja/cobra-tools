import contextlib
import logging
import struct
import time


def get_padding_size(size, alignment=16):
    mod = size % alignment
    if mod:
        return alignment - mod
    return 0


def get_padding(size, alignment=16):
    if alignment:
        # create the new blank padding
        return b"\x00" * get_padding_size(size, alignment=alignment)
    return b""


def djb2(s):
    # calculates djb2 hash for string s
    # from https://gist.github.com/mengzhuo/180cd6be8ba9e2743753#file-hash_djb2-py
    n = 5381
    for x in s:
        n = ((n << 5) + n) + ord(x)
    return n & 0xFFFFFFFF


def fnv64(data):
    hash_ = 0xcbf29ce484222325
    for b in data:
        hash_ *= 0x100000001b3
        hash_ &= 0xffffffffffffffff
        hash_ ^= b
    return hash_


def encode_int64_base32(integer, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ012345"):
    """Encodes a 64-bit integer into a base32 string with a custom charset."""
    encoded = ""
    while integer > 0:
        index = integer & 0x1F
        encoded += charset[index]
        integer >>= 5

    return encoded


def fmt_hash(id_hash):
    return "".join([f"{b:02X}" for b in struct.pack("<I", id_hash)])


class DummySignal:

    def emit(self, val):
        pass
        # logging.debug(f"Emitted {val}")

    def connect(self, func):
        pass


class DummyReporter:
    """A class wrapping the interaction between OvlFile and the UI"""
    warning_msg = DummySignal()  # type: ignore
    success_msg = DummySignal()  # type: ignore
    files_list = DummySignal()  # type: ignore
    included_ovls_list = DummySignal()  # type: ignore
    progress_percentage = DummySignal()  # type: ignore
    current_action = DummySignal()  # type: ignore

    def iter_progress(self, iterable, message):
        self.current_action.emit(message)
        self._percentage = 0
        v_max = len(iterable) - 1
        for i, item in enumerate(iterable):
            yield item
            if i and v_max:
                p = round(i / v_max * 100)
                if p != self._percentage:
                    self.progress_percentage.emit(p)
                    self._percentage = p
        msg = f"Finished {message}"
        self.current_action.emit(msg)
        # logging.success(msg)

    @contextlib.contextmanager
    def report_error_files(self, operation):
        error_files = []
        yield error_files
        if error_files:
            self.warning_msg.emit(
                (f"{operation} {len(error_files)} files failed - please check 'Show Details' or the log.",
                 "\n".join(error_files)))
        else:
            msg = f"{operation} succeeded"
            logging.success(msg)
            self.success_msg.emit(msg)

    def show_success(self, msg):
        logging.success(msg)
        self.success_msg.emit(msg)

    def show_error(self, msg, files=()):
        self.warning_msg.emit((msg, "\n".join(files)))

    @contextlib.contextmanager
    def log_duration(self, operation):
        logging.info(operation)
        start_time = time.time()
        yield
        duration = time.time() - start_time
        logging.debug(f"{operation} took {duration:.2f} seconds")
