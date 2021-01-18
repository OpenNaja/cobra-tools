# Experimental tool to create loc.ovl files for string localisation from a txt file
# only for JWE
# not a final modding tool, this is an experimental script

# input file is a text file with line entries, in name,value format, e.g.
# test1,this string
# test2,this other string
# doesntmatter,the length or the order of the strings.

# run: locovl_tool.py nameofthetextfile.txt  

# it will generate a loc.ovl file with those names and strings.

import zlib
import sys
import struct 

names  = []
values = []

compression = True

def ovl_header(entrycount, strsize):
	compressed = 0x6014 # default to not compress
	if compression == True:
		compressed = 0x6094
	return b"FRES" + struct.pack("<2H5I2H16I48s", 
		0x1301,0x100,
		compressed,0,strsize,0,0,
		0,1,
		entrycount, entrycount,0,1,1,1,0,0,0,0,0,0,8,entrycount,0x3f,0,
		b'')

def class_entry(entrycount): # has of FGDK:Text:text
	return struct.pack("<6I",0,0,0x262EA686,2,0,entrycount)
	
def ovs_header(entrycount, strsize, hashval):
	return struct.pack("<2H",3,1) + struct.pack("<8I",0,0,strsize,0,hashval,entrycount,0xb88b045,0)

def hash_djb2(s):                                                                                                                                
    hash = 5381
    for x in s:
        hash = (( hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF

def hash_name(data):
	val = data[0]
	return hash_djb2(data[0])

def getContent(filename):
	f = open(filename, 'r')
	content = f.readlines()
	f.close()
	return content

def processContent(lines):
	entries = []
	for line in lines:
		name, value = line.split(",", 1)
		djb2 = hash_djb2(name)
		entries.append([name,value.rstrip()])

	entries.sort(key=hash_name)
	return entries

# script start
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]


if len(args) > 0:
	content = getContent(args[0])
	if len(content) <= 0:
		raise SystemExit(
			f"{args[0]} is an invalid file\n"
		)

	count = len(content)
	if count <= 0:
		raise SystemExit(
			f"{args[0]} is in invalid format\n"
		)

	print(f"Processing {count} txt entries")
	items = processContent(content)

	# we have a list of items ordered by hash, make memory pools
	strpol1 = bytearray()
	strpol1 += b'FGDK:Text:txt\x00'

	strpol2 = bytearray()

	# build the list of entries as well
	ovlentries = []
	ovsentries = []
	for item in items:
		ovlentries.append([len(strpol1), hash_djb2(item[0])])
		ovsentries.append([len(strpol2), hash_djb2(item[0])])
		strpol1 += bytearray(item[0], encoding='utf8') + b"\x00"
		#strpol2 chunks are 8 byte aligned: size + data
		alignedval = struct.pack("<I", len(item[1])) + bytearray(item[1], encoding='utf8') + b"\x00"
		padding = 8 - (len(alignedval) % 8)
		if padding > 0:
			alignedval +=  struct.pack(f"{padding}s", b'')
		strpol2 += alignedval

	#our main output buffer, ovl part
	ovl  = ovl_header(len(ovlentries),len(strpol1)) + strpol1
	ovl += class_entry(len(ovlentries))
	for entry in ovlentries:
		ovl += struct.pack("<2I2H", entry[0],entry[1],1,0) 

	#main output buffer, ovs part, first item has defines the mem block
	ovs  = ovs_header(len(ovsentries), len(strpol2), ovsentries[0][1])
	for entry in ovsentries:
		ovs += struct.pack("<4I", entry[1],0xb88b045,0,entry[0]) 

	#endmarker:
	ovs += b"\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xBF\x7F\x3F\x08\x04\x02\x01"
	ovs += strpol2

	#quick glue, no compression
	poolhead = b'STATIC\x00\x00'
	mempool  = bytearray()
	ovsout   = bytearray()
	if compression == True:
		ovsout  = zlib.compress(ovs)
		mempool  = struct.pack("<4I2H12I", 
			0,0,0,1,
			0,1,
			0,0,0,len(ovsentries),0,0x10,len(ovsout),len(ovs),0,0,len(strpol2),0)
	else:
		ovsout = ovs
		mempool  = struct.pack("<4I2H12I", 
			0,0,0,1,
			0,1,
			0,0,0,len(ovsentries),0,0x10,len(ovsout),0,0,0,len(strpol2),0)

	poolinfo = struct.pack("<2I", len(strpol1)+len(strpol2),0)
	ovl += poolhead + mempool + poolinfo + ovsout

	ovlfile = open("Loc.ovl", "wb")
	ovlfile.write(ovl)
	ovlfile.close

	# debug save the ovs chunk
	#ovsfile = open("Loc.ovs", "wb")
	#ovsfile.write(ovsout)
	#ovsfile.close


else:
    raise SystemExit(
    	f"Usage: {sys.argv[0]} <options> [loc.txt]\n"
    	f"\nOptions:"
    	)
