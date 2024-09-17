# Initial draft tool to work on shader packages (arc files)
from io import BytesIO

import zlib
import sys
import struct


class xfxd3f(object):
    def __init__(self, data = b''):
        self.type = 'xfxd3f'
        self.header = b''
        self.fromBytes(data)

    def fromBytes(self, data):
        self.header = data[0:16]
        self.data = data[16:]
"""
xfxd3f data Pseudo structure.
struct {
 
  unsigned int64 header;
  unsigned int32 size;
   struct {
    struct {
      unsigned int32 size_T;
      unsigned int64 header;
      unsigned int32 size;
      unsigned int32 size_c;
      struct {
        unsigned int32 ints[size_c];
        unsigned char  data[size];
      } content;
    } voMrtp[2] <optimize=false>;
  } content;
  unsigned int32 size_T;

} data;

"""

class ahsd3f(object):
    def __init__(self, data = b''):
        self.type = 'xfxd3f'
        self.header = b''
        self.fromBytes(data)

    def fromBytes(self, data):
        self.header = data[0:16]
        self.data = data[16:]

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
        print(self.objectList[0].data)

     
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
        self.filePath = path

        # debug temp write content file
        f = open(path + ".uncomp", 'wb')
        f.write(data)
        f.close()

        # split the content into blobs
        offset = 0
        while offset < len(data):
            cheader = data[offset:offset+16]
            cvL, cvH, cmagic, ccompressedSize, cuncompressedSize = self.read_header(cheader)
            print(f"{cvL} {cvH} {cmagic} {ccompressedSize} {cuncompressedSize}")

            lobject = b''

            offset += ccompressedSize
            if cmagic == b"xfxd3f":
                lobject = xfxd3f(data[offset:offset+ccompressedSize])
                pass
            elif cmagic == b'ahsd3f':
                lobject = ahsd3f(data[offset:offset+ccompressedSize])
                pass
            else:
                print(f"Unknown magic type: {cmagic}")

            self.objectList.append(lobject)





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

"""
7 2 b'xfxd3f' 19560 0
5 2 b'ahsd3f' 4352 4264
5 2 b'ahsd3f' 1672 1584
7 2 b'xfxd3f' 24008 0
5 2 b'ahsd3f' 4520 4424
5 2 b'ahsd3f' 1664 1568
7 2 b'xfxd3f' 24080 0
5 2 b'ahsd3f' 5944 5848
5 2 b'ahsd3f' 17872 17776
5 2 b'ahsd3f' 19160 19064
5 2 b'ahsd3f' 21312 21216
5 2 b'ahsd3f' 18080 17984
5 2 b'ahsd3f' 19368 19272
5 2 b'ahsd3f' 21400 21304
5 2 b'ahsd3f' 21184 21088
5 2 b'ahsd3f' 22472 22376
5 2 b'ahsd3f' 25568 25472
5 2 b'ahsd3f' 21384 21288
5 2 b'ahsd3f' 22672 22576
5 2 b'ahsd3f' 25720 25624
5 2 b'ahsd3f' 6400 6304
5 2 b'ahsd3f' 22840 22744
5 2 b'ahsd3f' 24128 24032
5 2 b'ahsd3f' 26328 26232
5 2 b'ahsd3f' 23120 23024
5 2 b'ahsd3f' 24408 24312
5 2 b'ahsd3f' 26432 26336
5 2 b'ahsd3f' 26280 26184
5 2 b'ahsd3f' 27568 27472
5 2 b'ahsd3f' 30712 30616
5 2 b'ahsd3f' 26504 26408
5 2 b'ahsd3f' 27792 27696
5 2 b'ahsd3f' 30912 30816
7 2 b'xfxd3f' 32320 0
5 2 b'ahsd3f' 7384 7280
5 2 b'ahsd3f' 5552 5448
5 2 b'ahsd3f' 5752 5648
7 2 b'xfxd3f' 24528 0
5 2 b'ahsd3f' 5136 5040
5 2 b'ahsd3f' 5160 5064
5 2 b'ahsd3f' 5360 5264
7 2 b'xfxd3f' 24448 0
5 2 b'ahsd3f' 4400 4312
5 2 b'ahsd3f' 1512 1424
7 2 b'xfxd3f' 24008 0
5 2 b'ahsd3f' 5832 5736
5 2 b'ahsd3f' 1008 912
7 2 b'xfxd3f' 21600 0
5 2 b'ahsd3f' 1376 1280
7 2 b'xfxd3f' 24056 0
5 2 b'ahsd3f' 3096 3016
5 2 b'ahsd3f' 1056 976
7 2 b'xfxd3f' 21560 0
5 2 b'ahsd3f' 3184 3096
5 2 b'ahsd3f' 1104 1016
7 2 b'xfxd3f' 21544 0
5 2 b'ahsd3f' 6520 6440
5 2 b'ahsd3f' 19576 19496
5 2 b'ahsd3f' 19720 19640
5 2 b'ahsd3f' 22992 22912
5 2 b'ahsd3f' 23136 23056
5 2 b'ahsd3f' 6976 6896
5 2 b'ahsd3f' 24632 24552
5 2 b'ahsd3f' 24872 24792
5 2 b'ahsd3f' 28120 28040
5 2 b'ahsd3f' 28344 28264
7 2 b'xfxd3f' 27448 0
5 2 b'ahsd3f' 6464 6368
5 2 b'ahsd3f' 3584 3488
5 2 b'ahsd3f' 3704 3608
7 2 b'xfxd3f' 23256 0
5 2 b'ahsd3f' 4568 4480
5 2 b'ahsd3f' 3192 3104
5 2 b'ahsd3f' 3312 3224
7 2 b'xfxd3f' 23168 0
5 2 b'ahsd3f' 4840 4760
7 2 b'xfxd3f' 21536 0
5 2 b'ahsd3f' 1176 1096
7 2 b'xfxd3f' 21576 0
5 2 b'ahsd3f' 3696 3616
7 2 b'xfxd3f' 21600 0
5 2 b'ahsd3f' 3824 3728
7 2 b'xfxd3f' 21608 0
5 2 b'ahsd3f' 24096 24008
5 2 b'ahsd3f' 25416 25328
5 2 b'ahsd3f' 27368 27280
5 2 b'ahsd3f' 24296 24208
5 2 b'ahsd3f' 25656 25568
5 2 b'ahsd3f' 27472 27384
5 2 b'ahsd3f' 27320 27232
5 2 b'ahsd3f' 28648 28560
5 2 b'ahsd3f' 31544 31456
5 2 b'ahsd3f' 27520 27432
5 2 b'ahsd3f' 28856 28768
5 2 b'ahsd3f' 31640 31552
5 2 b'ahsd3f' 28952 28864
5 2 b'ahsd3f' 30264 30176
5 2 b'ahsd3f' 32248 32160
5 2 b'ahsd3f' 29160 29072
5 2 b'ahsd3f' 30464 30376
5 2 b'ahsd3f' 32360 32272
5 2 b'ahsd3f' 32304 32216
5 2 b'ahsd3f' 33584 33496
5 2 b'ahsd3f' 36528 36440
5 2 b'ahsd3f' 32504 32416
5 2 b'ahsd3f' 33784 33696
5 2 b'ahsd3f' 36696 36608
7 2 b'xfxd3f' 35128 0
5 2 b'ahsd3f' 9848 9744
5 2 b'ahsd3f' 10048 9944
7 2 b'xfxd3f' 27424 0
5 2 b'ahsd3f' 9456 9360
5 2 b'ahsd3f' 9656 9560
7 2 b'xfxd3f' 27344 0
5 2 b'ahsd3f' 3752 3664
7 2 b'xfxd3f' 21600 0
7 2 b'xfxd3f' 21592 0
7 2 b'xfxd3f' 21616 0
7 2 b'xfxd3f' 21608 0
7 2 b'xfxd3f' 21608 0
5 2 b'ahsd3f' 23736 23640
5 2 b'ahsd3f' 25056 24960
5 2 b'ahsd3f' 26912 26816
5 2 b'ahsd3f' 23936 23840
5 2 b'ahsd3f' 25256 25160
5 2 b'ahsd3f' 27112 27016
5 2 b'ahsd3f' 26984 26888
5 2 b'ahsd3f' 28264 28168
5 2 b'ahsd3f' 31072 30976
5 2 b'ahsd3f' 27192 27096
5 2 b'ahsd3f' 28464 28368
5 2 b'ahsd3f' 31280 31184
5 2 b'ahsd3f' 28592 28496
5 2 b'ahsd3f' 29960 29864
5 2 b'ahsd3f' 31848 31752
5 2 b'ahsd3f' 28800 28704
5 2 b'ahsd3f' 30160 30064
5 2 b'ahsd3f' 32056 31960
5 2 b'ahsd3f' 31944 31848
5 2 b'ahsd3f' 33248 33152
5 2 b'ahsd3f' 36048 35952
5 2 b'ahsd3f' 32144 32048
5 2 b'ahsd3f' 33456 33360
5 2 b'ahsd3f' 36272 36176
7 2 b'xfxd3f' 34576 0
5 2 b'ahsd3f' 8912 8808
5 2 b'ahsd3f' 9112 9008
7 2 b'xfxd3f' 26872 0
5 2 b'ahsd3f' 8528 8432
5 2 b'ahsd3f' 8728 8632
7 2 b'xfxd3f' 26792 0
7 2 b'xfxd3f' 21608 0
7 2 b'xfxd3f' 21592 0
7 2 b'xfxd3f' 21616 0
7 2 b'xfxd3f' 21600 0
7 2 b'xfxd3f' 21600 0
5 2 b'ahsd3f' 23496 23408
5 2 b'ahsd3f' 24736 24648
5 2 b'ahsd3f' 26656 26568
5 2 b'ahsd3f' 23640 23552
5 2 b'ahsd3f' 24944 24856
5 2 b'ahsd3f' 26912 26824
5 2 b'ahsd3f' 26672 26584
5 2 b'ahsd3f' 27944 27856
5 2 b'ahsd3f' 30840 30752
5 2 b'ahsd3f' 26872 26784
5 2 b'ahsd3f' 28152 28064
5 2 b'ahsd3f' 31080 30992
5 2 b'ahsd3f' 28432 28344
5 2 b'ahsd3f' 29720 29632
5 2 b'ahsd3f' 31576 31488
5 2 b'ahsd3f' 28632 28544
5 2 b'ahsd3f' 29888 29800
5 2 b'ahsd3f' 31776 31688
5 2 b'ahsd3f' 31784 31696
5 2 b'ahsd3f' 33088 33000
5 2 b'ahsd3f' 35792 35704
5 2 b'ahsd3f' 31872 31784
5 2 b'ahsd3f' 33248 33160
5 2 b'ahsd3f' 35976 35888
7 2 b'xfxd3f' 34488 0
7 2 b'xfxd3f' 21600 0
7 2 b'xfxd3f' 21608 0
5 2 b'ahsd3f' 22776 22688
5 2 b'ahsd3f' 24184 24096
5 2 b'ahsd3f' 26072 25984
5 2 b'ahsd3f' 22984 22896
5 2 b'ahsd3f' 24272 24184
5 2 b'ahsd3f' 26256 26168
5 2 b'ahsd3f' 26128 26040
5 2 b'ahsd3f' 27416 27328
5 2 b'ahsd3f' 30240 30152
5 2 b'ahsd3f' 26216 26128
5 2 b'ahsd3f' 27512 27424
5 2 b'ahsd3f' 30312 30224
5 2 b'ahsd3f' 27712 27624
5 2 b'ahsd3f' 29128 29040
5 2 b'ahsd3f' 31016 30928
5 2 b'ahsd3f' 27920 27832
5 2 b'ahsd3f' 29176 29088
5 2 b'ahsd3f' 31072 30984
5 2 b'ahsd3f' 31128 31040
5 2 b'ahsd3f' 32416 32328
5 2 b'ahsd3f' 35240 35152
5 2 b'ahsd3f' 31304 31216
5 2 b'ahsd3f' 32592 32504
5 2 b'ahsd3f' 35432 35344
7 2 b'xfxd3f' 34328 0
5 2 b'ahsd3f' 8904 8800
5 2 b'ahsd3f' 9104 9000
7 2 b'xfxd3f' 26568 0
5 2 b'ahsd3f' 8512 8416
5 2 b'ahsd3f' 8712 8616
7 2 b'xfxd3f' 26488 0
7 2 b'xfxd3f' 21600 0
7 2 b'xfxd3f' 21592 0
7 2 b'xfxd3f' 21616 0
5 2 b'ahsd3f' 8896 8800
5 2 b'ahsd3f' 9096 9000
7 2 b'xfxd3f' 26744 0
5 2 b'ahsd3f' 8504 8416
5 2 b'ahsd3f' 8704 8616
7 2 b'xfxd3f' 26664 0
7 2 b'xfxd3f' 21600 0
7 2 b'xfxd3f' 21584 0
7 2 b'xfxd3f' 21608 0
5 2 b'ahsd3f' 5336 5248
5 2 b'ahsd3f' 15272 15184
5 2 b'ahsd3f' 16560 16472
5 2 b'ahsd3f' 19104 19016
5 2 b'ahsd3f' 20392 20304
5 2 b'ahsd3f' 19104 19016
5 2 b'ahsd3f' 16128 16040
5 2 b'ahsd3f' 17416 17328
5 2 b'ahsd3f' 19952 19864
5 2 b'ahsd3f' 21240 21152
7 2 b'xfxd3f' 29848 0
5 2 b'ahsd3f' 656 576
7 2 b'xfxd3f' 20592 0
5 2 b'ahsd3f' 2904 2824
7 2 b'xfxd3f' 20968 0
5 2 b'ahsd3f' 3216 3144
7 2 b'xfxd3f' 21184 0
7 2 b'xfxd3f' 21192 0
5 2 b'ahsd3f' 3512 3416
7 2 b'xfxd3f' 21768 0
5 2 b'ahsd3f' 3200 3112
5 2 b'ahsd3f' 2552 2464
5 2 b'ahsd3f' 3840 3752
5 2 b'ahsd3f' 5080 4992
5 2 b'ahsd3f' 7064 6976
5 2 b'ahsd3f' 8352 8264
7 2 b'xfxd3f' 23376 0
7 2 b'xfxd3f' 21760 0
5 2 b'ahsd3f' 3032 2952
5 2 b'ahsd3f' 2136 2056
5 2 b'ahsd3f' 3424 3344
5 2 b'ahsd3f' 4928 4848
5 2 b'ahsd3f' 6664 6584
5 2 b'ahsd3f' 7936 7856
7 2 b'xfxd3f' 23280 0
5 2 b'ahsd3f' 7680 7584
5 2 b'ahsd3f' 2120 2024
7 2 b'xfxd3f' 23096 0
5 2 b'ahsd3f' 8072 7968
5 2 b'ahsd3f' 2000 1896
7 2 b'xfxd3f' 23232 0
5 2 b'ahsd3f' 10472 10368
5 2 b'ahsd3f' 20272 20168
5 2 b'ahsd3f' 21560 21456
5 2 b'ahsd3f' 20472 20368
5 2 b'ahsd3f' 21760 21656
5 2 b'ahsd3f' 23576 23472
5 2 b'ahsd3f' 24864 24760
5 2 b'ahsd3f' 23784 23680
5 2 b'ahsd3f' 25072 24968
5 2 b'ahsd3f' 10808 10704
5 2 b'ahsd3f' 25392 25288
5 2 b'ahsd3f' 26680 26576
5 2 b'ahsd3f' 25600 25496
5 2 b'ahsd3f' 26888 26784
5 2 b'ahsd3f' 28776 28672
5 2 b'ahsd3f' 30064 29960
5 2 b'ahsd3f' 28984 28880
5 2 b'ahsd3f' 30272 30168
7 2 b'xfxd3f' 31136 0
5 2 b'ahsd3f' 10144 10032
5 2 b'ahsd3f' 7984 7872
5 2 b'ahsd3f' 8184 8072
7 2 b'xfxd3f' 23552 0
5 2 b'ahsd3f' 9760 9656
5 2 b'ahsd3f' 7592 7488
5 2 b'ahsd3f' 7792 7688
7 2 b'xfxd3f' 23528 0
5 2 b'ahsd3f' 7632 7520
5 2 b'ahsd3f' 1544 1432
7 2 b'xfxd3f' 23096 0
5 2 b'ahsd3f' 7808 7712
5 2 b'ahsd3f' 1872 1776
7 2 b'xfxd3f' 23096 0
5 2 b'ahsd3f' 2272 2184
7 2 b'xfxd3f' 22920 0
5 2 b'ahsd3f' 2160 2056
7 2 b'xfxd3f' 23040 0
5 2 b'ahsd3f' 20000 19904
5 2 b'ahsd3f' 21288 21192
5 2 b'ahsd3f' 20200 20104
5 2 b'ahsd3f' 21488 21392
5 2 b'ahsd3f' 23304 23208
5 2 b'ahsd3f' 24592 24496
5 2 b'ahsd3f' 23512 23416
5 2 b'ahsd3f' 24800 24704
5 2 b'ahsd3f' 25128 25032
5 2 b'ahsd3f' 26416 26320
5 2 b'ahsd3f' 25328 25232
5 2 b'ahsd3f' 26616 26520
5 2 b'ahsd3f' 28512 28416
5 2 b'ahsd3f' 29800 29704
5 2 b'ahsd3f' 28712 28616
5 2 b'ahsd3f' 30000 29904
7 2 b'xfxd3f' 30904 0
5 2 b'ahsd3f' 8536 8424
5 2 b'ahsd3f' 8736 8624
7 2 b'xfxd3f' 23440 0
5 2 b'ahsd3f' 8144 8040
5 2 b'ahsd3f' 8344 8240
7 2 b'xfxd3f' 23416 0
5 2 b'ahsd3f' 1704 1592
7 2 b'xfxd3f' 22920 0
5 2 b'ahsd3f' 2032 1936
7 2 b'xfxd3f' 22920 0
5 2 b'ahsd3f' 2112 2024
7 2 b'xfxd3f' 22776 0
5 2 b'ahsd3f' 1992 1896
7 2 b'xfxd3f' 22896 0
5 2 b'ahsd3f' 20264 20168
5 2 b'ahsd3f' 21552 21456
5 2 b'ahsd3f' 20464 20368
5 2 b'ahsd3f' 21752 21656
5 2 b'ahsd3f' 23568 23472
5 2 b'ahsd3f' 24856 24760
5 2 b'ahsd3f' 23776 23680
5 2 b'ahsd3f' 25064 24968
5 2 b'ahsd3f' 25384 25288
5 2 b'ahsd3f' 26672 26576
5 2 b'ahsd3f' 25592 25496
5 2 b'ahsd3f' 26880 26784
5 2 b'ahsd3f' 28768 28672
5 2 b'ahsd3f' 30056 29960
5 2 b'ahsd3f' 28976 28880
5 2 b'ahsd3f' 30264 30168
7 2 b'xfxd3f' 30688 0
5 2 b'ahsd3f' 7976 7872
5 2 b'ahsd3f' 8176 8072
7 2 b'xfxd3f' 23216 0
5 2 b'ahsd3f' 7584 7488
5 2 b'ahsd3f' 7784 7688
7 2 b'xfxd3f' 23192 0
5 2 b'ahsd3f' 7624 7520
5 2 b'ahsd3f' 1536 1432
7 2 b'xfxd3f' 22784 0
5 2 b'ahsd3f' 1864 1776
7 2 b'xfxd3f' 22776 0
5 2 b'ahsd3f' 2264 2184
7 2 b'xfxd3f' 22600 0
5 2 b'ahsd3f' 2152 2056
7 2 b'xfxd3f' 22752 0
5 2 b'ahsd3f' 19992 19904
5 2 b'ahsd3f' 21280 21192
5 2 b'ahsd3f' 20192 20104
5 2 b'ahsd3f' 21480 21392
5 2 b'ahsd3f' 23296 23208
5 2 b'ahsd3f' 24584 24496
5 2 b'ahsd3f' 23504 23416
5 2 b'ahsd3f' 24792 24704
5 2 b'ahsd3f' 25120 25032
5 2 b'ahsd3f' 26408 26320
5 2 b'ahsd3f' 25320 25232
5 2 b'ahsd3f' 26608 26520
5 2 b'ahsd3f' 28504 28416
5 2 b'ahsd3f' 29792 29704
5 2 b'ahsd3f' 28704 28616
5 2 b'ahsd3f' 29992 29904
7 2 b'xfxd3f' 30480 0
5 2 b'ahsd3f' 8528 8424
5 2 b'ahsd3f' 8728 8624
7 2 b'xfxd3f' 23136 0
5 2 b'ahsd3f' 8136 8040
5 2 b'ahsd3f' 8336 8240
7 2 b'xfxd3f' 23112 0
5 2 b'ahsd3f' 1696 1592
7 2 b'xfxd3f' 22608 0
5 2 b'ahsd3f' 2024 1936
7 2 b'xfxd3f' 22600 0
5 2 b'ahsd3f' 7568 7488
5 2 b'ahsd3f' 2128 2048
7 2 b'xfxd3f' 23552 0
5 2 b'ahsd3f' 4968 4880
5 2 b'ahsd3f' 1208 1120
7 2 b'xfxd3f' 22944 0
5 2 b'ahsd3f' 6992 6896
5 2 b'ahsd3f' 16312 16216
5 2 b'ahsd3f' 17600 17504
5 2 b'ahsd3f' 16512 16416
5 2 b'ahsd3f' 17800 17704
5 2 b'ahsd3f' 19408 19312
5 2 b'ahsd3f' 20696 20600
5 2 b'ahsd3f' 19608 19512
5 2 b'ahsd3f' 20896 20800
5 2 b'ahsd3f' 7104 7008
5 2 b'ahsd3f' 21256 21160
5 2 b'ahsd3f' 22544 22448
5 2 b'ahsd3f' 21464 21368
5 2 b'ahsd3f' 22752 22656
5 2 b'ahsd3f' 24424 24328
5 2 b'ahsd3f' 25712 25616
5 2 b'ahsd3f' 24624 24528
5 2 b'ahsd3f' 25872 25776
7 2 b'xfxd3f' 30928 0
5 2 b'ahsd3f' 7168 7056
5 2 b'ahsd3f' 6672 6560
5 2 b'ahsd3f' 6872 6760
7 2 b'xfxd3f' 23832 0
5 2 b'ahsd3f' 6176 6072
5 2 b'ahsd3f' 6288 6184
5 2 b'ahsd3f' 6488 6384
7 2 b'xfxd3f' 23736 0
5 2 b'ahsd3f' 6336 6232
5 2 b'ahsd3f' 6880 6776
5 2 b'ahsd3f' 7560 7456
7 2 b'xfxd3f' 23680 0
5 2 b'ahsd3f' 5024 4928
5 2 b'ahsd3f' 1216 1120
7 2 b'xfxd3f' 23200 0
5 2 b'ahsd3f' 5696 5600
7 2 b'xfxd3f' 22992 0
5 2 b'ahsd3f' 6424 6336
5 2 b'ahsd3f' 1744 1656
7 2 b'xfxd3f' 23672 0
5 2 b'ahsd3f' 9392 9304
5 2 b'ahsd3f' 18360 18272
5 2 b'ahsd3f' 19648 19560
5 2 b'ahsd3f' 18560 18472
5 2 b'ahsd3f' 19848 19760
5 2 b'ahsd3f' 21672 21584
5 2 b'ahsd3f' 22960 22872
5 2 b'ahsd3f' 21880 21792
5 2 b'ahsd3f' 23168 23080
5 2 b'ahsd3f' 9496 9408
5 2 b'ahsd3f' 23488 23400
5 2 b'ahsd3f' 24776 24688
5 2 b'ahsd3f' 23688 23600
5 2 b'ahsd3f' 24976 24888
5 2 b'ahsd3f' 26872 26784
5 2 b'ahsd3f' 28160 28072
5 2 b'ahsd3f' 27072 26984
5 2 b'ahsd3f' 28360 28272
7 2 b'xfxd3f' 31432 0
5 2 b'ahsd3f' 10128 10032
5 2 b'ahsd3f' 6512 6416
5 2 b'ahsd3f' 6712 6616
7 2 b'xfxd3f' 24200 0
5 2 b'ahsd3f' 8896 8808
5 2 b'ahsd3f' 6736 6648
5 2 b'ahsd3f' 6936 6848
7 2 b'xfxd3f' 24104 0
5 2 b'ahsd3f' 7216 7128
7 2 b'xfxd3f' 23560 0
5 2 b'ahsd3f' 6072 5968
7 2 b'xfxd3f' 23688 0
5 2 b'ahsd3f' 9096 9000
5 2 b'ahsd3f' 9200 9104
7 2 b'xfxd3f' 31440 0
5 2 b'ahsd3f' 9840 9728
7 2 b'xfxd3f' 24216 0
5 2 b'ahsd3f' 8608 8504
7 2 b'xfxd3f' 24120 0
5 2 b'ahsd3f' 2376 2264
5 2 b'ahsd3f' 1240 1128
7 2 b'xfxd3f' 22592 0
5 2 b'ahsd3f' 8656 8552
5 2 b'ahsd3f' 7392 7288
5 2 b'ahsd3f' 8096 7992
7 2 b'xfxd3f' 24200 0
5 2 b'ahsd3f' 7272 7176
5 2 b'ahsd3f' 1648 1552
7 2 b'xfxd3f' 23496 0
5 2 b'ahsd3f' 7760 7664
7 2 b'xfxd3f' 23328 0
5 2 b'ahsd3f' 2728 2632
7 2 b'xfxd3f' 22584 0
5 2 b'ahsd3f' 8944 8856
7 2 b'xfxd3f' 24184 0
5 2 b'ahsd3f' 7616 7536
7 2 b'xfxd3f' 23488 0
5 2 b'ahsd3f' 8128 8048
7 2 b'xfxd3f' 23320 0
5 2 b'ahsd3f' 4704 4616
7 2 b'xfxd3f' 21576 0
5 2 b'ahsd3f' 16232 16136
5 2 b'ahsd3f' 17520 17424
5 2 b'ahsd3f' 16432 16336
5 2 b'ahsd3f' 17720 17624
5 2 b'ahsd3f' 19328 19232
5 2 b'ahsd3f' 20616 20520
5 2 b'ahsd3f' 19528 19432
5 2 b'ahsd3f' 20816 20720
5 2 b'ahsd3f' 21056 20960
5 2 b'ahsd3f' 22344 22248
5 2 b'ahsd3f' 21264 21168
5 2 b'ahsd3f' 22552 22456
5 2 b'ahsd3f' 24200 24104
5 2 b'ahsd3f' 25512 25416
5 2 b'ahsd3f' 24424 24328
5 2 b'ahsd3f' 25696 25600
5 2 b'ahsd3f' 25712 25616
7 2 b'xfxd3f' 30848 0
5 2 b'ahsd3f' 6672 6560
5 2 b'ahsd3f' 6872 6760
7 2 b'xfxd3f' 23752 0
5 2 b'ahsd3f' 6288 6184
5 2 b'ahsd3f' 6488 6384
7 2 b'xfxd3f' 23656 0
5 2 b'ahsd3f' 6880 6776
5 2 b'ahsd3f' 7560 7456
7 2 b'xfxd3f' 23600 0
5 2 b'ahsd3f' 4752 4664
7 2 b'xfxd3f' 21576 0
7 2 b'xfxd3f' 22912 0
5 2 b'ahsd3f' 5744 5664
7 2 b'xfxd3f' 21816 0
5 2 b'ahsd3f' 5960 5872
5 2 b'ahsd3f' 1104 1016
7 2 b'xfxd3f' 23144 0
5 2 b'ahsd3f' 9504 9416
5 2 b'ahsd3f' 17504 17416
5 2 b'ahsd3f' 18792 18704
5 2 b'ahsd3f' 17712 17624
5 2 b'ahsd3f' 19000 18912
5 2 b'ahsd3f' 20872 20784
5 2 b'ahsd3f' 22160 22072
5 2 b'ahsd3f' 21072 20984
5 2 b'ahsd3f' 22360 22272
5 2 b'ahsd3f' 9608 9520
5 2 b'ahsd3f' 22528 22440
5 2 b'ahsd3f' 23816 23728
5 2 b'ahsd3f' 22728 22640
5 2 b'ahsd3f' 24016 23928
5 2 b'ahsd3f' 25912 25824
5 2 b'ahsd3f' 27200 27112
5 2 b'ahsd3f' 26112 26024
5 2 b'ahsd3f' 27400 27312
7 2 b'xfxd3f' 31184 0
5 2 b'ahsd3f' 9928 9832
5 2 b'ahsd3f' 6736 6640
5 2 b'ahsd3f' 6936 6840
7 2 b'xfxd3f' 24088 0
5 2 b'ahsd3f' 8712 8624
5 2 b'ahsd3f' 7160 7072
5 2 b'ahsd3f' 7360 7272
7 2 b'xfxd3f' 23992 0
5 2 b'ahsd3f' 5320 5232
7 2 b'xfxd3f' 21832 0
5 2 b'ahsd3f' 5592 5488
7 2 b'xfxd3f' 23152 0
5 2 b'ahsd3f' 9216 9112
5 2 b'ahsd3f' 9320 9216
7 2 b'xfxd3f' 31200 0
5 2 b'ahsd3f' 9640 9528
7 2 b'xfxd3f' 24096 0
5 2 b'ahsd3f' 8424 8320
7 2 b'xfxd3f' 24000 0
5 2 b'ahsd3f' 8472 8368
5 2 b'ahsd3f' 7232 7128
5 2 b'ahsd3f' 7944 7840
7 2 b'xfxd3f' 23952 0
5 2 b'ahsd3f' 5376 5280
7 2 b'xfxd3f' 21832 0
5 2 b'ahsd3f' 7576 7480
7 2 b'xfxd3f' 23224 0
5 2 b'ahsd3f' 8760 8672
7 2 b'xfxd3f' 23936 0
5 2 b'ahsd3f' 5792 5712
7 2 b'xfxd3f' 21816 0
5 2 b'ahsd3f' 7952 7872
7 2 b'xfxd3f' 23208 0
5 2 b'ahsd3f' 3832 3744
5 2 b'ahsd3f' 3832 3744
5 2 b'ahsd3f' 5240 5152
5 2 b'ahsd3f' 8304 8216
7 2 b'xfxd3f' 22680 0
7 2 b'xfxd3f' 20952 0
5 2 b'ahsd3f' 1096 1000
7 2 b'xfxd3f' 21752 0
5 2 b'ahsd3f' 5736 5648
5 2 b'ahsd3f' 15672 15584
5 2 b'ahsd3f' 16960 16872
5 2 b'ahsd3f' 15784 15696
5 2 b'ahsd3f' 17040 16952
5 2 b'ahsd3f' 19504 19416
5 2 b'ahsd3f' 20792 20704
5 2 b'ahsd3f' 19616 19528
5 2 b'ahsd3f' 20936 20848
5 2 b'ahsd3f' 6208 6120
5 2 b'ahsd3f' 20704 20616
5 2 b'ahsd3f' 21992 21904
5 2 b'ahsd3f' 20936 20848
5 2 b'ahsd3f' 22224 22136
5 2 b'ahsd3f' 24496 24408
5 2 b'ahsd3f' 25784 25696
5 2 b'ahsd3f' 24728 24640
5 2 b'ahsd3f' 26016 25928
7 2 b'xfxd3f' 30216 0
5 2 b'ahsd3f' 6712 6608
5 2 b'ahsd3f' 3232 3128
5 2 b'ahsd3f' 3408 3304
"""