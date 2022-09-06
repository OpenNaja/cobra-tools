import io
import logging

from generated.formats.dds.enums.D3D10ResourceDimension import D3D10ResourceDimension
from generated.formats.dds.enums.FourCC import FourCC
from generated.formats.dds.structs.Dxt10Header import Dxt10Header
from generated.formats.dds.structs.Header import Header
from generated.io import IoFile
from modules.formats.shared import get_padding, get_padding_size


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

    def load(self, filepath):
        with open(filepath, "rb") as stream:
            self.read_fields(stream, self)
            self.buffer = stream.read()

    def save(self, filepath):
        with open(filepath, "wb") as stream:
            self.write_fields(stream, self)
            stream.write(self.buffer)

    def get_bytes_size(self, num_pixels):
        return int(round(num_pixels / self.pixels_per_byte))

    def calculate_mip_sizes(self):
        logging.info("Calculating mip map sizes")
        self.get_pixel_fmt()
        tiles = []
        for array_i in range(self.dx_10.array_size):
            tile_mips = []
            h = self.height
            w = self.width
            tiles.append(tile_mips)
            for mip_i in range(self.mipmap_count):
                # go per tile
                # note that array_size is not set by texconv
                num_pixels = h * w
                # read at least one block
                num_bytes = max(self.block_byte_size, self.get_bytes_size(num_pixels))
                logging.debug(f"Tile {array_i} Mip {mip_i} with {num_pixels} pixels, {num_bytes} bytes")
                tile_mips.append((h, w, num_bytes))
                h //= 2
                w //= 2
        return tiles

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

    def mip_pack_generator(self, mip_infos):
        """Yields data size to be read from stream + amount of padding applied for packed representation)"""
        tiles_per_mips = zip(*self.calculate_mip_sizes())
        mip_offset = 0
        for mip_i, (tiles_per_mip, mip_info) in enumerate(zip(tiles_per_mips, mip_infos)):
            # mip_offset = stream.tell()
            for tile_i, (height, width, tile_byte_size) in enumerate(tiles_per_mip):
                bytes_width = self.get_bytes_size(width)
                # logging.debug(f"tile {tile_i}, offset {mip_info.offset} {mip_offset}, height {height}, width {width}")
                # logging.debug(f"width {width}, bytes width {bytes_width}")
                if bytes_width > 32:
                    yield tile_byte_size, 0
                    mip_offset += tile_byte_size
                    # logging.debug(f"Wrote mip {mip_i} for tile {tile_i}, {len(tile_bytes)} raw bytes")
                else:
                    # no matter what pixel size the mips represent, they must be at least one 4x4 chunk
                    height = max(self.block_len_pixels_1d, height)

                    # write horizontal lines
                    # get count of h slices, 1 block is 4x4 px
                    num_slices_y = height // self.block_len_pixels_1d
                    bytes_per_line = tile_byte_size // num_slices_y
                    padding_per_line = get_padding_size(bytes_per_line, alignment=256)

                    # logging.debug(
                    #     f"num_slices_y {num_slices_y}, bytes_per_line {bytes_per_line}, padding_per_line {padding_per_line}")
                    # write the bytes for this line from the mip bytes
                    for slice_i in range(num_slices_y):
                        # get the bytes that represent the blocks of this line and fill the line with padding blocks
                        yield bytes_per_line, padding_per_line
                        mip_offset += bytes_per_line
                        mip_offset += padding_per_line

                    # add one fully blank line for those cases
                    if num_slices_y == 1:
                        yield 0, 256
                        mip_offset += 256
                    #
                    # logging.debug(
                    #     f"Packed mip {mip_i} for tile {tile_i}, {len(tile_bytes)} raw bytes, {num_slices_y} Y slices, {stream.tell() - mip_offset} total bytes")

    def pack_mips(self, mip_infos):
        """From a standard DDS stream, pack the lower mip levels into one image and pad with empty bytes"""
        logging.info("Packing mip maps")
        dds = io.BytesIO(self.buffer)
        with io.BytesIO() as tex:
            for data_size, padding_size in self.mip_pack_generator(mip_infos):
                # logging.info(f"Writing {data_size}, padding {padding_size}")
                tex.write(dds.read(data_size))
                tex.write(b"\x00" * padding_size)
            return tex.getvalue()

    def unpack_mips(self, mip_infos, tex_buffer_data):
        """Restore standard DDS mip stream, unpack the lower mip levels by discarding the padding"""
        logging.info("Unpacking mip maps")
        tex = io.BytesIO(tex_buffer_data)
        with io.BytesIO() as dds:
            for data_size, padding_size in self.mip_pack_generator(mip_infos):
                # logging.info(f"Writing {data_size}, skipping {padding_size}")
                data = tex.read(data_size)
                dds.write(data)
                padding = tex.read(padding_size)
                if padding != b"\x00" * len(padding):
                    logging.warning(f"Tex padding is non-zero at {tex.tell()-padding_size}")
            return dds.getvalue()

    def pack_mips_pc(self, buffer_infos):
        """Grab the lower mip levels according to the count"""
        tiles_per_mips = list(zip(*self.calculate_mip_sizes()))
        mip_cuts = [self.mipmap_count - b.num_mips for b in buffer_infos]
        # print(mip_cuts)
        buffers = []
        for mip_0 in mip_cuts:
            # get the size for all tiles of the valid mip levels
            bytes_size = sum([tile[2] for mip in tiles_per_mips[mip_0:] for tile in mip])
            # print(mip_0, bytes_size, tile_sizes)
            buffers.append(self.buffer[-bytes_size:])
        return buffers


if __name__ == "__main__":
    m = DdsFile()
    print(m)
    # m.load("C:/Users/arnfi/Desktop/parrot/parrot.pbasecolourtexture.dds")
