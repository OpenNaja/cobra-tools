# Initial draft tool to work on shader packages (arc files)
from io import BytesIO

import zlib
import sys
import struct

header_str  = b''
data_offset = 0
compressed  = False

class Archive(object):
    def __init__(self, objectList = [], useCompression=True, filePath=''):
        self.useCompression = useCompression
        self.filePath       = filePath
        self.objectList     = objectList
        self.content        = b""
        self.vL             = 0
        self.vH             = 1
        self.magic          = b'talfed'


    def setCompression(self, useCompression):
        self.useCompression = useCompression

    def print_details(self):
        print( 'Archive Details:')
        print(f'   object count: {len(self.objectList)}')
        print(f'     file path : {self.filePath}')
        print(f' is compressed : {self.useCompression}')

     
    def list_objects(self):
        print('Listing Objects:')

    def read_header(self, content):
        return struct.unpack("<2B6s2I", content[0:16])

    def write_header(self, vL, vH, magic, compressedSize, uncompressedSize):
        return struct.pack("<2B6s2I", vL, vH, magic, compressedSize, uncompressedSize)

    def loadFrom(self, path):
        print(f'Loading: {path}')

        # read file contents
        f = open(path, 'rb')
        content = f.read()
        f.close()

        # validate header
        vL, vH, magic, compressedSize, uncompressedSize = self.read_header(content)
        print(f"File header: {magic} version {vH}.{vL}")
        assert vL == 0, "Invalid file version"
        assert vH == 1, "Invalid file version"
        assert magic == self.magic, "Invalid file id"

        compressed = True if uncompressedSize > 0 else False

        # decompress content
        if compressed:
            data = zlib.decompress(content[16:], -15)
        assert len(data) == uncompressedSize, "Decompression failed"

        # we arrived here, we can save the data
        self.content = data
        self.useCompression = compressed

        # debug temp write content file
        f = open(path + ".uncomp", 'wb')
        f.write(data)
        f.close()

        # split the content into blobs


    def saveAs(self, path):
        print(f'Saving: {path}')
        # read file contents
        f = open(path, 'wb')

        data = self.content
        uncompressedSize = len(data)
        compressedSize = 0

        if self.useCompression:
            compress = zlib.compressobj(1, zlib.DEFLATED, -15)
            compressed_data  = compress.compress(self.content)
            compressed_data += compress.flush()
            data = compressed_data
            compressedSize = len(data)

        f.write(self.write_header(self.vL, self.vH, self.magic, compressedSize, uncompressedSize) )
        f.write(data)
        f.close()


    def save(self):
    	self.saveAs(self.filePath)


opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

#default output.intput name
if len(args) > 1:
    name =  args[1]

if   "-e" in opts:   # export
    pass
elif "-i" in opts: # import
    pass
elif "-l" in opts: # load the file, debug make an uncompressed copy
    archive1 = Archive()
    archive1.loadFrom(args[0])
    archive1.print_details()
    pass

else:
	raise SystemExit(
		f"Usage: {sys.argv[0]} (-l | -e | -i) <file>...\n\n"
		f"-e\tExport shaders from archive\n"
		f"-i\tImport shaders to archive\n"
		f"-l\tList archive information\n"
		f"\n"
		)

