# Experimental tool to create an ovl files with lua files from the disk
# only for JWE, supporting: fdb, lua, assetpkg and userinterfaceicondata.
# not a final modding tool, this is an experimental script

# input is a folder with the lua files on it. It will create a ovl file
# with the same name as the folder.

# run: lua_tool.py path_to_folder_with_luas  

import os
import xml.etree.ElementTree as ET
import uuid

import zlib
import sys
import struct 


#whether generated ovl files are compressed or not
compression = True

# builds manifest file name
def manifest_name(name):
	return name.rstrip('/') + "/Manifest.xml"

# creates mod xml 
def manifest_content(name):
	data = ET.Element('ContentPack')
	data.set('version', '1')

	mname = ET.SubElement(data, 'Name')
	mname.text = name

	mid = ET.SubElement(data, 'ID')
	mid.text = str(uuid.uuid1())

	mver = ET.SubElement(data, 'Version')
	mver.text = "1"

	mtype = ET.SubElement(data, 'Type')
	mtype.text = "Game"

	return ET.tostring(data).decode('utf-8')

# returns name entry from manifest file
def name_from_manifest(name):
	tree = ET.parse(manifest_name(name))
	root = tree.getroot()
	elms = tree.findall('.//Name') 
	if len(elms) > 0:
		return elms[0].text
	else:
		raise SystemExit(
			f"mod name not found in {name} manifest file.\n"
		)		

# creates folder and adds manifes file
def mod_create(name):
	#modname should not include path info
	modname = os.path.basename(name)
	# strip right slash
	if os.path.isfile(manifest_name(name)) and 1==0:
		raise SystemExit(
			f"{name} folder mod already exists\n"
		)		
	else:
		if not os.path.exists(name):
			os.makedirs(name)

		f = open(manifest_name(name), "w")
		f.write(manifest_content(modname))
		f.close()
		raise SystemExit(
			f"{name} mod folder created\n"
		)		

# add specific starting lua scripts
# removed to avoid having to publish game content
def mod_add_luas(name, modname):
	return

# add specific starting db files
# removed to avoid having to publish game content
def mod_add_fdbs(name, modname):
	return

# add default mod structure to the mod folder
def mod_default(name):
	# we either exited if -create failed or reach this point
	if os.path.isfile(manifest_name(name)):
		
		# get the mod name from the manifest
		modname = name_from_manifest(name)
		print(f"Found {modname} Manifest")

		if not os.path.exists(name + '/Init'):
			os.makedirs(name + '/Init')		
		if not os.path.exists(name + '/Main'):
			os.makedirs(name + '/Main')		

		# keep adding default mod files:
		mod_add_luas(name, modname)
		mod_add_fdbs(name, modname)

		raise SystemExit(
			f"{name} default files added\n"
		)		
	else:
		raise SystemExit(
			f"{name} Manifest not found in this folder, use -create first.\n"
		)		

# reads a file
def getContent(filename):
	f = open(filename, 'rb')
	content = f.read()
	f.close()
	return content

# writes a file 
def setContent(filename, content):
	f = open(filename, "wb")
	f.write(content)
	f.close()

# pack folders into ovl files
def folder_pack(basepath):
	files = []
	for entry in os.listdir(basepath):
		if os.path.isdir(os.path.join(basepath, entry)):
			folder_pack(os.path.join(basepath, entry))
		else:
			if entry.endswith('.lua') or entry.endswith('.fdb') or entry.endswith('.assetpkg') or entry.endswith('.userinterfaceicondata'):
				files.append(entry.lower())

	#ignore current folder if there are no known files
	#print(basepath, files)    
	if len(files) > 0:
		ovlname = os.path.basename(basepath)
		print(f"Creating: {ovlname}.ovl")

		content = files_pack(files, basepath)
		setContent(basepath + ".ovl", content)

	return

# calculate djb2hash
def hash_djb2(s):   
    hash = 5381
    for x in s:
        hash = (( hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF

#return has of name in [name, data] tuple
def hash_name(data):
	val = data[0]
	return hash_djb2(data[0])

# given a list of file names, return a sorted array of only names
def sorted_namelist(data):
	entries = []
	for entry in data:
		name = os.path.splitext(entry)[0]
		djb2 = hash_djb2(name)
		entries.append([name,entry])
	entries.sort(key=hash_name)
	return entries

def buffer_padding(dbuffer, length):
	blen = len(dbuffer) % length
	if blen > 0:
		dbuffer += struct.pack(f"{length-blen}s", b'')	
	return dbuffer

# pack files in a dir into an ovl
def files_pack(files, basepath):

	fdbs = [fdb for fdb in files if fdb.endswith(".fdb")]
	luas = [lua for lua in files if lua.endswith(".lua")]
	asse = [ass for ass in files if ass.endswith('.assetpkg')]
	uics = [uic for uic in files if uic.endswith('.userinterfaceicondata')]

	classes = []
	entries = []

	# initial ovl state
	strzpool   = b''
	offset     = 0
	classcount = 0
	entrycount = 0

	#order is assetpkg, fdb, lua 
	if len(asse) > 0:
		classes.append([len(strzpool), 0x444B295A, 2, entrycount, len(asse)])
		strzpool += b"Casino:AssetPackageRes:assetpkg" + b'\x00'
		entrycount += len(asse)
	if len(fdbs) > 0:
		classes.append([len(strzpool), 0x97B8DB21, 1, entrycount, len(fdbs)])
		strzpool += b"FGDK:Database:fdb" + b'\x00'
		entrycount += len(fdbs)
	if len(luas) > 0:
		classes.append([len(strzpool), 0x6A0A84F0, 7, entrycount, len(luas)])
		strzpool += b"FGDK:LuaModule:lua" + b'\x00'
		entrycount += len(luas)
	if len(uics) > 0:
		classes.append([len(strzpool), 0x7ED198C7, 1, entrycount, len(uics)])
		strzpool += b"Casino:UserInterfaceIconData:userinterfaceicondata" + b'\x00'
		entrycount += len(uics)

	# restart counters to process entries
	offset     = len(strzpool)
	entrycount = 0
	bufferscount = 0

	asssorted = []
	fdbsorted = []
	luasorted = []
	uicsorted = []


	if len(asse) > 0:
		# order names by hash
		asssorted = sorted_namelist(asse)
		for ass in asssorted:
			print(f"+ {ass[0]}.assetpkg")
			entries.append([len(strzpool), hash_djb2(ass[0]), 4, classcount, ass[1], 0x444B295A, ass[0]])
			strzpool += bytearray(ass[0], encoding='utf8') + b'\x00'
		classcount   += 1
		entrycount   += len(asssorted)
		#bufferscount += len(asssorted)

	if len(fdbs) > 0:
		fdbsorted = sorted_namelist(fdbs)
		for fdb in fdbsorted:
			print(f"+ {fdb[0]}.fdb")
			entries.append([len(strzpool), hash_djb2(fdb[0]), 4, classcount, fdb[1], 0x97B8DB21, fdb[0]])
			strzpool += bytearray(fdb[0], encoding='utf8') + b'\x00'
		classcount   += 1
		entrycount   += len(fdbsorted)
		bufferscount += len(fdbsorted)

	if len(luas) > 0:
		luasorted = sorted_namelist(luas)
		for lua in luasorted:
			print(f"+ {lua[0]}.lua")
			entries.append([len(strzpool), hash_djb2(lua[0]), 2, classcount, lua[1], 0x6A0A84F0, lua[0]])
			strzpool += bytearray(lua[0], encoding='utf8') + b'\x00'
		entrycount   += len(luasorted)
		bufferscount += len(luasorted)
		classcount += 1

	if len(uics) > 0:
		uicsorted = sorted_namelist(uics)
		for uic in uicsorted:
			print(f"+ {uic[0]}.userinterfaceicondata")
			entries.append([len(strzpool), hash_djb2(uic[0]), 4, classcount, uic[1], 0x7ED198C7, uic[0]])
			strzpool += bytearray(uic[0], encoding='utf8') + b'\x00'
		entrycount   += len(uicsorted)
		#bufferscount += len(uicsorted)
		classcount += 1		

	# ovl finished, now the OVS
	ovs = b''

	# all classes go in a memory block
	memblock = b''
	offset   = 0

	# load the content of the files for the buffers/miniblocks section
	blockex = []
	blockmi = []
	buffers = []
	ovsentries = []
	pointers = []
	for entry in entries:
		# load the file contents
		dbuffer = getContent(basepath + '/' + entry[4])
		
		if entry[5] == 0x444B295A: # assetpkg.. copy content, pad to 64b, then assign 1 ptr.
			dbuffer = buffer_padding(dbuffer + b'\x00',64)
			memblock += dbuffer
			memblock += struct.pack('8s', b'') #ptr
			memblock += struct.pack('8s', b'')
			pointers.append([0, offset + len(dbuffer), 0 , offset])
			ovsentries.append([entry[1] ,0xA8B4AFC7, 0,  offset + len(dbuffer)] )
			# no blockex

		if entry[5] == 0x97B8DB21: # fdb
			memblock += struct.pack("I28s",  len(dbuffer), b'')
			#no pointers
			ovsentries.append([entry[1] , 0xB887211, 0, offset])
			buffers.append(dbuffer)
			blockex.append([entry[1], 0xB887211, 0, 2, 0, len(dbuffer) + len(entry[6]), 0,0,0])
			blockmi.append([1, len(dbuffer)])
			blockmi.append([0, len(entry[6])])

		if entry[5] == 0x6A0A84F0: # lua if this is an id we need to randomize it
			memblock += struct.pack("IIII",  len(dbuffer), 16000, 0x00, 0x00)
			memblock += struct.pack("24s", b'') # room for 3 pointers
			memblock += struct.pack("8s", b'')  # room for 2 ints
			memblock += b'\x00' #one more char for the 2nd ptr
			memblock += bytearray(entry[6], encoding='utf8') + b'\x00'
			pointers.append([0, offset + 0x10, 0 , offset + 0x31]) #ptr to name
			pointers.append([0, offset + 0x18, 0 , offset + 0x30]) #ptr to deleted name
			ovsentries.append([entry[1] , 0xB888DC7, 0, offset])

			buffers.append(dbuffer)
			blockex.append([entry[1],  0xB888DC7, 0, 1, 0, len(dbuffer), 0,0,0])
			blockmi.append([0, len(dbuffer)])

		if entry[5] == 0x7ED198C7: # userinterfaceiconddata, needs 2 pointers for 2 strings

			icname, icpath = dbuffer.split(b',')
			outb = icname + b'\x00' + icpath + b'\x00'
			outb = buffer_padding(outb, 64) + struct.pack('8s', b'')
			memblock += outb
			newoffset = len(memblock)
			memblock += struct.pack('8s', b'') # two pointers
			memblock += struct.pack('8s', b'') # two pointers
			iclen = len(outb)
			pointers.append([0, newoffset, 0 , offset])
			pointers.append([0, newoffset + 8, 0 , offset + len(icname) + 1])
			ovsentries.append([entry[1] ,0x603D40F8, 0,  newoffset ] )

		#next ovs entry start needs to be padded to 4 bytes
		memblock = buffer_padding(memblock, 4)
		offset = len(memblock)

	# finally add blockex/mi buffers:
	for fdb in fdbsorted:
		buffers.append(bytearray(fdb[0], encoding='utf8'))


	# write all to the ovs
	for exblock in blockex:
		a,b,c,d,e,f,g,h,i = exblock
		ovs += struct.pack("IIHHIIIII", a,b,c,d,e,f,g,h,i)
	for miblock in blockmi:
		a,b = miblock
		ovs += struct.pack("II", a,b)
	for entry in ovsentries:
		a,b,c,d = entry
		ovs += struct.pack("IIII", a,b,c,d)
	for pointer in pointers:
		a,b,c,d = pointer
		ovs += struct.pack("IIII", a,b,c,d)


	ovs += b"\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xBF\x7F\x3F\x08\x04\x02\x01"
	ovs += memblock
	b = b''
	ovs += b.join(buffers)


	# can now write the ovl header, class and entry list
	newcontent = ovl_header(len(strzpool), classcount, entrycount, len(blockex), len(buffers)) + strzpool

	for eclass in classes:
		newcontent += struct.pack( "6I", eclass[0], 0, eclass[1], eclass[2], eclass[3], eclass[4] )

	for entry in entries:
		newcontent += struct.pack( "2I2H", entry[0], entry[1], entry[2], entry[3] )

	ovl = newcontent

	# now form the ovs
	ovshead  = ovs_header(len(ovsentries), len(memblock), ovsentries[0][1], ovsentries[0][0])
	ovs = ovshead + ovs

	#quick glue, no compression
	poolhead = b'STATIC\x00\x00'
	mempool  = bytearray()
	ovsout   = bytearray()
	if compression == True:
		ovsout  = zlib.compress(ovs)
		mempool  = struct.pack("<4I2H12I", 
			0,0,0,1,
			len(blockex),1,
			0,len(buffers),len(pointers),len(ovsentries),0,0x10,len(ovsout),len(ovs),0,0,len(memblock),0)
	else:
		ovsout = ovs
		mempool  = struct.pack("<4I2H12I", 
			0,0,0,1,
			len(blockex),1,
			0,len(buffers),len(pointers),len(ovsentries),0,0x10,len(ovsout),0,0,0,len(memblock),0)

	poolinfo = struct.pack("<2I", len(ovs)+len(mempool),0)
	ovl += poolhead + mempool + poolinfo + ovsout

	newcontent = ovl

	return newcontent 

# craft ovl header
def ovl_header(strsize, classcount, entrycount, blockexcount, bufferscount):
	compressed = 0x6014 # default to not compress
	if compression == True:
		compressed = 0x6094
	return b"FRES" + struct.pack("<2H5I2H16I48s", 
		0x1301,0x100,
		compressed,
		0,
		strsize,
		0,0,0,
		classcount,
		entrycount, 
		entrycount,
		0,
		1, #mem pools
		1, #blocktypecount
		1, #ovsblocks
		blockexcount,
		bufferscount,
		0,0,0,0,8,
		entrycount,0x3f,0,
		b'')

#craft ovs header
def ovs_header(entrycount, strsize, hashval, blockhash):

	return struct.pack("<2H",2,1) + struct.pack("<8I",0,0,strsize,0,blockhash,entrycount,hashval,0)


# script start
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

# cleaning entry
if len(args) >0:
	args[0] = args[0].rstrip('/')

# checking args
if "-create" in opts:
	if len(args) <= 0:
		raise SystemExit(
			f"Valid syntax is: {args[0]} -create 'modname'\n"
		)
	else:
		# create mod folder and 
		mod_create(args[0])
		raise SystemExit()

if "-default" in opts:
	if len(args) <= 0:
		raise SystemExit(
			f"Valid syntax is: {args[0]} -default 'modname'\n"
		)
	else:
		# create mod folder and 
		mod_default(args[0])

# we created a mod, or added default files, 
if "-create" in opts or "-default" in opts:
		raise SystemExit()

if len(args) > 0:
	for entry in os.listdir(args[0]):
		path = os.path.join(args[0], entry)
		if os.path.isdir(path):
			folder_pack(path)
	raise SystemExit(
		f"Done."
		)
else:
    raise SystemExit(
    	f"Usage: {sys.argv[0]} <options> modname\n"
    	f"\nOptions:\n"
    	f" -create   will create the folder and manifest file.\n"
    	f" -default  will add default folder and files to the mod folder.\n"
    	f" -pack     will create the ovl files\n"
    	)
