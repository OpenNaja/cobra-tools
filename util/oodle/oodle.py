import os
from ctypes import cdll, c_char_p, create_string_buffer


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
            raise Exception(
                "Could not load Oodle DLL, requires Windows and 64bit python to run."
            ) from e

    def compress(self, payload: bytes, algorithm: int = 9) -> bytes:
        """
        Compress the payload using the given algorithm.
        """
        input_size = len(payload)
        output_size = input_size
        output = create_string_buffer(output_size)
        # OodleLZ_Compress(10, in, insz, out, 7, NULL, NULL, NULL);
        ret = self.handle.OodleLZ_Compress(
            algorithm, c_char_p(payload), input_size, output, 8, None, None, None, None, 0
        )

        # print("input size", input_size, "Output size", ret)
        # # Make sure the result length matches the given output size
        # if ret != output_size:
        #     raise Exception(
        #         "Decompression failed ret=0x{:x} output_size=0x{:x}".format(ret, output_size)
        #     )

        return output.raw[:ret]

    def decompress(self, payload: bytes, size: int, output_size: int) -> bytes:
        """
        Decompress the payload using the given size.
        """
        output = create_string_buffer(output_size)

        ret = self.handle.OodleLZ_Decompress(
            c_char_p(payload), size, output, output_size,
            0, 0, 0, None, None, None, None, None, None, 3
        )

        # Make sure the result length matches the given output size
        if ret != output_size:
            raise Exception(
                "Decompression failed ret=0x{:x} output_size=0x{:x}".format(ret, output_size)
            )

        return output.raw
