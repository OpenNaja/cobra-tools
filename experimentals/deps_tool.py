# Experimental tool to add/remove dependecies on OVL files
# not a final modding tool, this is an experimental script
# run: desp_tool.py file.ovl +data/test
# run: desp_tool.py file.ovl +../../data/test
# run: desp_tool.py file.ovl -data/test

# only use path without extensions
# it will add or remove a dependency to the ovl to require that new ovl file

import zlib
import sys
import struct 

adds = {}
rems = {}
args = {}

def getContent(filename):
	f = open(filename, 'rb')
	content = f.read()
	f.close()
	return content

def setContent(filename, data):
	print(f"Writting: {filename}")
	f = open(filename, 'wb')
	f.write(data)
	f.close()

def ovl_read_header(data):
	strzpoolsz  = struct.unpack( "<I", data[16:20])
	foldercount = struct.unpack( "<H", data[28:30])
	classcount  = struct.unpack( "<H", data[30:32])
	poolscount  = struct.unpack( "<I", data[44:48])
	entriescount= struct.unpack( "<I", data[32:36])
	return strzpoolsz[0], foldercount[0], classcount[0], entriescount[0], poolscount[0]

def ovl_write_header(data, strzpoolsz, foldercount):
	return data[0:16] + struct.pack("I", strzpoolsz) + data[20:28] + struct.pack("H", foldercount) + data[30:0x90]


def ovl_list_path(content):
	strzpoolsz, foldercount, classcount, entriescount, poolscount = ovl_read_header(content)
	stringpool = content[0x90:0x90+strzpoolsz]
	offset = 0x90 + strzpoolsz + 6*4* classcount + 3*4* entriescount + 8 + 68*poolscount

	if foldercount > 0:
		print("Dependencies:")
	else:
		print("No dependencies found")
		return

	for index in range(foldercount):
		entryoffset = struct.unpack("<I", content[offset:offset+4])[0]
		path = stringpool[entryoffset:].split(b'\0',1)[0].decode('utf-8')
		print(f" {path}")
		offset += 4
	return

def ovl_find_path(content, path):
	strzpoolsz, foldercount, classcount, entriescount, poolscount = ovl_read_header(content)
	stringpool = content[0x90:0x90+strzpoolsz]
	offset = 0x90 + strzpoolsz + 6*4* classcount + 3*4* entriescount + 8 + 68*poolscount

	if foldercount > 0:
		for index in range(foldercount):
			entryoffset = struct.unpack("<I", content[offset:offset+4])[0]
			filepath = stringpool[entryoffset:].split(b'\0',1)[0].decode('utf-8')
			if filepath == path[1:]:
				return index, entryoffset
			offset += 4
	
	return -1,-1

def ovl_add_path(content, path):
	print(f"Adding: {path[1:]}")

	strzpoolsz, foldercount, classcount, entriescount, poolscount = ovl_read_header(content)
	stringpool = content[0x90:0x90+strzpoolsz]

	#prepend the new entry
	entryname  = bytearray(add[1:], encoding='utf8') + b'\x00'
	entrylen   = len(entryname)
	outputpool = entryname + stringpool

	newcontent = ovl_write_header(content, len(outputpool), (foldercount + 1)) + outputpool

	#update class  list
	offset = 0x90 + strzpoolsz
	for index in range(classcount):
		oldoffset = struct.unpack( "<I", content[offset:offset+4])[0]
		newcontent +=  struct.pack("I", oldoffset + entrylen) + content[offset + 4:offset + 4 + 5*4]
		offset += 6*4


	#update file list
	for index in range(entriescount):
		oldoffset = struct.unpack( "<I", content[offset:offset+4])[0]
		newcontent +=  struct.pack("I", oldoffset + entrylen) + content[offset + 4:offset + 4 + 2*4]
		offset += 3*4

	# need to copy mempools here!!
	newcontent += content[offset: offset + 8 + poolscount*68 ]
	offset += 8 + poolscount * 68

	#add our own folder entry now:
	newcontent += struct.pack("I", 0)

	#update folder list
	foldersoffset = offset + 4
	for index in range(foldercount):
		oldoffset = struct.unpack( "<I", content[offset:offset+4])[0]
		newcontent +=  struct.pack("I", oldoffset + entrylen)
		offset += 4

	newcontent += content[offset:]
	return newcontent
   

def ovl_rem_path(content, path):
	print(f"Removing: {path[1:]}")

	#find the path entry first..
	pindex, poffset = ovl_find_path(content, path)
	if pindex < 0:
		print(f"Entry {path} not found as dependency")
		return content

	#process the file to remove the entry
	strzpoolsz, foldercount, classcount, entriescount, poolscount = ovl_read_header(content)
	stringpool = content[0x90:0x90+strzpoolsz]

	#found the entry, then we have to remove it
	entryname  = bytearray(path[1:], encoding='utf8') + b'\x00'
	entrylen   = len(entryname)

	outputpool = stringpool[0:poffset] + stringpool[poffset+entrylen:] 
	newcontent = ovl_write_header(content, len(outputpool), (foldercount - 1)) + outputpool

	#update class  list
	offset = 0x90 + strzpoolsz
	for index in range(classcount):
		oldoffset = struct.unpack( "<I", content[offset:offset+4])[0]
		if oldoffset > poffset:
			newcontent +=  struct.pack("I", oldoffset - entrylen) + content[offset + 4:offset + 4 + 5*4]
		else:
			newcontent += content[offset:offset+6*4]
		offset += 6*4


	#update file list
	for index in range(entriescount):
		oldoffset = struct.unpack( "<I", content[offset:offset+4])[0]
		if oldoffset > poffset:
			newcontent +=  struct.pack("I", oldoffset - entrylen) + content[offset + 4:offset + 4 + 2*4]
		else:
			newcontent += content[offset:offset+3*4]
		offset += 3*4

	# need to copy mempools here!!
	newcontent += content[offset: offset + 8 + poolscount*68 ]
	offset += 8 + poolscount * 68

	#update folder list
	foldersoffset = offset + 4
	for index in range(foldercount):
		oldoffset = struct.unpack( "<I", content[offset:offset+4])[0]
		if pindex != index:
			if oldoffset > poffset:
				newcontent +=  struct.pack("I", oldoffset - entrylen)
			else:
				newcontent += content[offset:offset+4]
		offset += 4

	newcontent += content[offset:]
	return newcontent



adds = [add for add in sys.argv[1:] if add.startswith("+")]
rems = [rem for rem in sys.argv[1:] if rem.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-") and not arg.startswith("+")]

print(adds)
print(rems)
print(args)


if len(args) > 0:
	content = getContent(args[0])
	if len(content) <= 0:
		raise SystemExit(
			f"{args[0]} is an invalid file\n"
		)

	if content[:4] != b"FRES":
		raise SystemExit(
			f"{args[0]} is not an ovl file\n"
		)

	print(f"Processing file")

	for add in adds:
		content = ovl_add_path(content, add)

	for rem in rems:
		content = ovl_rem_path(content, rem)

	if (len(adds) + len(rems)) == 0:
		ovl_list_path(content)
		print("listed")
	else:
		#write file
		setContent(args[0], content)

else:
	raise SystemExit(
		f"Usage: {sys.argv[0]} [+path] [-path] file.ovl\n"
	)
