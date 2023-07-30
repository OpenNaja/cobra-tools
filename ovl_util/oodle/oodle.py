import os
import logging
from ctypes import cdll, c_char_p, create_string_buffer
from enum import IntEnum

# taken from quickbms oodle.c
compressions = (
    ("LZH",            0,  7),
    ("LZHLW",          1,  0),
    ("LZNIB",          2,  1),
    ("None",           3,  7),    # 0x8c->0xcc
    ("LZB16",          4,  2),
    ("LZBLW",          5,  3),
    ("LZA",            6,  4),
    ("LZNA",           7,  5),
    ("Kraken",         8,  6),
    ("Mermaid",        9, 10),
    ("BitKnit",       10, 11),
    ("Selkie",        11, 10),
    ("Hydra",         12,  6),
    ("Leviathan",     13, 12),
    ("NONE", -1, -1))

OodleCompressEnum = IntEnum('OodleEnum', list([(x[0], x[1]) for x in compressions]))
OodleDecompressEnum = IntEnum('OodleEnum', list([(x[0], x[2]) for x in compressions]))

oodle_dll = os.path.join(os.path.dirname(__file__), "oo2core_8_win64.dll")


class OodleDecompressor:
    """
    Oodle decompression implementation.
    Requires Windows and the external Oodle library.
    """

    def __init__(self, library_path: str) -> None:
        """
        Initialize instance and try to load the library.
        """
        if not os.path.exists(library_path):
            raise Exception("Could not open Oodle DLL, make sure it is configured correctly.")

        try:
            self.handle = cdll.LoadLibrary(library_path)
        except OSError as e:
            raise Exception("Could not load Oodle DLL, requires Windows and 64bit python to run.") from e

    def compress(self, payload: bytes, algorithm_name: str, level: int = 7) -> bytes:
        """
        Compress the payload using the given algorithm.
        """
        algorithm = OodleCompressEnum[algorithm_name]
        logging.debug(f"Compressing as {algorithm_name} (value = {algorithm.value}), level = {level}")
        input_size = len(payload)
        output_size = self.get_compressed_bounds(input_size)
        output = create_string_buffer(output_size)
        compressed_size = self.handle.OodleLZ_Compress(
            algorithm.value, c_char_p(payload), input_size, output, level, None, None, None, None, 0)
        logging.debug(f"Oodle compressed {input_size} bytes down to {compressed_size} bytes.")
        if input_size and not compressed_size:
            raise ValueError("Oodle Compression returned no payload for unknown reason!")
        return output.raw[:compressed_size]

    def decompress(self, payload: bytes, size: int, output_size: int) -> bytes:
        """
        Decompress the payload using the given size.
        """
        output = create_string_buffer(output_size)
        ret = self.handle.OodleLZ_Decompress(
            c_char_p(payload), size, output, output_size,
            0, 0, 0, None, None, None, None, None, None, 3)

        # Make sure the result length matches the given output size
        if ret != output_size:
            raise Exception(f"Decompression failed ret={ret} output_size={output_size}")

        return output.raw

    @staticmethod
    def get_compressed_bounds(uncompressed_size):
        return int(uncompressed_size + 274 * ((uncompressed_size + 0x3FFFF) / 0x400000))


oodle_compressor = OodleDecompressor(oodle_dll)
