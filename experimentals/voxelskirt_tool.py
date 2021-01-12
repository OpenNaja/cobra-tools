# Experimental tool to remove the limits of the buildable area in a voxelskirt
# of a JWE world. Not tested with voxelskirts of other games
# not a final modding tool, this is an experimental script
import zlib
import sys
import struct 

#OVL_GUI_TOOL adds its custom metadata to the voxelskirt struct that needs to be 
#accounted for on every offset
headerskip = 132

#return int64 from data:offset
def getInt64(data, offset):
	return int.from_bytes(data[offset:offset+8], byteorder='little', signed=False) 

#get number of layers
def getNameCount(data):
	namecount =  int.from_bytes(data[124:132], byteorder='little', signed=False) 
	return namecount

#given index, return name
def getName(data, index):
	namelist =  int.from_bytes(data[116:124], byteorder='little', signed=False) + headerskip
	offset = namelist + index * 8 
	namepos  = int.from_bytes(data[offset:offset+8], byteorder='little', signed=False) + headerskip
	name = data[namepos:namepos+32].split(b'\x00')[0]
	return name

#given name, return offset of data struct
def findStructByName(data, name):
	structlist = int.from_bytes(data[52:60], byteorder='little', signed=False) + headerskip
	count = getNameCount(data)
	for x in range(0, count):
		offset = structlist + x * 4 * 8 
		nid = int.from_bytes(data[offset:offset+8], byteorder='little', signed=False) 
		bname = getName(data, nid)
		sname = bytearray(name, encoding='utf8')
		if bname == sname:
			return offset
	return -1

#display voxelskirt information
def printInfo(data):
	structlist = int.from_bytes(data[52:60], byteorder='little', signed=False) + headerskip
	count = getNameCount(data)
	for x in range(0, count):
		offset  = structlist + x * 4 * 8 
		nid = getInt64(content, offset)
		stype   = getInt64(content, offset + 8)
		soffset = getInt64(content, offset + 16) + headerskip
		size    = getInt64(content, offset + 24)
		bname   = getName(data, nid)
		print(f"{nid} : {bname}")
	return


# script start
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if len(args) > 0:
	content = open(args[0], 'rb').read()
	if content[0:4] != b'VOXE':
		raise SystemExit(
			f"{args[0]} is not a voxelskirtfile\n\n"
		)

    #display voxelskirt information
	printInfo(content)

	if len(args)<2:
		raise SystemExit(
			f"No map selected\n"
		)

	#default map is nature
	usemap = b'nature'
	if len(args) > 1:
		usemap = args[1]

    #default value is 0xff
	usevalue = "0"
	if len(args) > 2:
		usevalue = args[2]

	# find the location of this map name
	dstruct = findStructByName(content, usemap)
	if dstruct == -1:
		raise SystemExit(
			f"map {args[1]} not found in {args[0]}\n\n"
		)

	# get map data
	stype  = getInt64(content, dstruct + 8)
	offset = getInt64(content, dstruct + 16) + headerskip
	size   = getInt64(content, dstruct + 24)

	#modify the map bytes
	data = bytearray(content)
	if stype == 0:
		for x in range(0, size):
			data[offset+x] = int(usevalue, base=10)
	elif stype == 2:
		for x in range(0, size):
			fvalue = bytearray(struct.pack("f", int(usevalue, base=10)))  
			data[offset+x*4:offset+x*4+4] = fvalue
	else:
		raise SystemExit(
			f"Unknown map data type\n"
			f"\n"
			)

	#save voxelskirt
	f = open(args[0], 'wb')
	f.write(data)
	f.close()


else:
    raise SystemExit(
    	f"Usage: {sys.argv[0]} <voxelskirtfile> [mapname] [value]...\n\n"
    	f"\n"
    	)

