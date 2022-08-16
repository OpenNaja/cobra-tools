import io
import logging

from generated.formats.dds.enums.D3D10ResourceDimension import D3D10ResourceDimension
from generated.formats.dds.enums.FourCC import FourCC
from generated.formats.dds.structs.Dxt10Header import Dxt10Header
from generated.formats.dds.structs.Header import Header
from generated.io import IoFile
from modules.formats.shared import get_padding


class DdsContext(object):
    def __init__(self):
        self.version = 0
        self.user_version = 0

    def __repr__(self):
        return f"{self.version} | {self.user_version}"


class DdsFile(Header, IoFile):

    def __init__(self, ):
        super().__init__(DdsContext())
        self.header_string.data = b"DDS "

        # header flags
        self.flags.height = 1
        self.flags.width = 1
        self.flags.mipmap_count = 1
        self.flags.linear_size = 1

        # pixel format flags
        self.pixel_format.flags.four_c_c = 1
        self.pixel_format.four_c_c = FourCC.DX10

        self.dx_10 = Dxt10Header(self.context, 0, None)
        self.dx_10.resource_dimension = D3D10ResourceDimension.D3D10_RESOURCE_DIMENSION_TEXTURE2D
        self.dx_10.array_size = 1

        # caps 1
        self.caps_1.texture = 0

        # other stuff
        self.buffer = b""
        self.tiles = []

    def load(self, filepath):
        with open(filepath, "rb") as stream:
            self.read_fields(stream, self)
            self.read_mips(stream)

    def save(self, filepath):
        with open(filepath, "wb") as stream:
            self.write_fields(stream, self)
            stream.write(self.buffer)

    def get_bytes_size(self, num_pixels):
        return int(round(num_pixels / self.pixels_per_byte))

    def read_mips(self, stream):
        logging.info("Reading mip maps")
        self.get_pixel_fmt()
        self.tiles.clear()
        mips_start = stream.tell()
        for array_i in range(self.dx_10.array_size):
            tile_mips = []
            h = self.height
            w = self.width
            self.tiles.append(tile_mips)
            for mip_i in range(self.mipmap_count):
                # go per tile
                # note that array_size is not set by texconv
                num_pixels = h * w
                # read at least one block
                num_bytes = max(self.block_byte_size, self.get_bytes_size(num_pixels))
                logging.debug(f"Tile {array_i} Mip {mip_i} at {stream.tell()} ({stream.tell()-mips_start}), {num_pixels} pixels, {num_bytes} bytes")
                tile_mips.append((h, w, stream.read(num_bytes)))
                h //= 2
                w //= 2
        # print(self.mips)
        # self.buffer = b"".join([b"".join(level_bytes_per_tile) for h, w, level_bytes_per_tile in self.mips])
        self.buffer = b"".join([level_bytes for tile in self.tiles for h, w, level_bytes in tile])
        logging.debug(f"End of mips at {stream.tell()}")

    def get_pixel_fmt(self):
        # get compression type
        comp = self.dx_10.dxgi_format.name
        # get bpp from compression type
        if "R8G8B8A8" in comp:
            self.pixels_per_byte = 0.25
            self.block_len_pixels_1d = 1
        elif "BC1" in comp or "BC4" in comp:
            self.pixels_per_byte = 2
            self.block_len_pixels_1d = 4
        else:
            self.pixels_per_byte = 1
            self.block_len_pixels_1d = 4
        # a block is the smallest usable unit, for dxt it is 4x4 px, for RGBA it is 1x1 px
        # get its byte count
        self.block_byte_size = int(round(self.block_len_pixels_1d * self.block_len_pixels_1d / self.pixels_per_byte))
        logging.debug(f"Compression: {comp}")
        logging.debug(f"pixels_per_byte: {self.pixels_per_byte}")
        logging.debug(f"block_len_pixels_1d: {self.block_len_pixels_1d}")
        logging.debug(f"block_byte_size: {self.block_byte_size}")

    def pack_mips(self, mip_infos):
        """From a standard DDS stream, pack the lower mip levels into one image and pad with empty bytes"""
        logging.info("Packing mip maps")
        with io.BytesIO() as stream:
            tiles_per_mips = zip(*self.tiles)

            for mip_i, (tiles_per_mip, mip_info) in enumerate(zip(tiles_per_mips, mip_infos)):
                mip_offset = stream.tell()

                for tile_i, (height, width, tile_bytes) in enumerate(tiles_per_mip):
                    bytes_width = self.get_bytes_size(width)
                    logging.debug(f"offset {mip_info.offset}, {mip_offset}")
                    logging.debug(f"width {width}, bytes width {bytes_width}")
                    if bytes_width > 32:
                        stream.write(tile_bytes)
                        logging.debug(f"Wrote mip {mip_i} for tile {tile_i}, {len(tile_bytes)} raw bytes")
                    else:
                        # no matter what pixel size the mips represent, they must be at least one 4x4 chunk
                        height = max(self.block_len_pixels_1d, height)

                        # write horizontal lines
                        # get count of h slices, 1 block is 4x4 px
                        num_slices_y = height // self.block_len_pixels_1d
                        bytes_per_line = len(tile_bytes) // num_slices_y

                        # write the bytes for this line from the mip bytes
                        for slice_i in range(num_slices_y):
                            # get the bytes that represent the blocks of this line
                            sl = tile_bytes[slice_i * bytes_per_line: (slice_i + 1) * bytes_per_line]
                            stream.write(sl)
                            # fill the line with padding blocks
                            stream.write(get_padding(len(sl), alignment=256))

                        # add one fully blank line for those cases
                        if num_slices_y == 1:
                            stream.write(b"\x00" * 256)

                        logging.debug(f"Packed mip {mip_i} for tile {tile_i}, {len(tile_bytes)} raw bytes, {num_slices_y} Y slices, {stream.tell()-mip_offset} total bytes")

            return stream.getvalue()

    def pack_mips_pc(self, num_mips):
        """Grab the lower mip levels according to the count"""
        first_mip_index = self.mipmap_count - num_mips
        print("first mip", first_mip_index)

        # get final merged output bytes
        return b"".join([b for h, w, b in self.mips[first_mip_index:]])


if __name__ == "__main__":
    m = DdsFile()
    print(m)
    # m.load("C:/Users/arnfi/Desktop/parrot/parrot.pbasecolourtexture.dds")
