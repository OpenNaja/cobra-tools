import logging
import os
import tempfile
import shutil
import subprocess
import struct

util_dir = os.path.dirname(__file__)
BINARY = os.path.normpath(os.path.join(util_dir, "texconv/texconv.exe"))
ww2ogg = os.path.normpath(os.path.join(util_dir, "ww2ogg/ww2ogg.exe"))
pcb = os.path.normpath(os.path.join(util_dir, "ww2ogg/packed_codebooks_aoTuV_603.bin"))
revorb = os.path.normpath(os.path.join(util_dir, "revorb/revorb.exe"))
luadec = os.path.normpath(os.path.join(util_dir, "luadec/luadec.exe"))
luac = os.path.normpath(os.path.join(util_dir, "luadec/luac.exe"))


def run_smart(args):
	# argline = " ".join(['"' + x + '"' for x in args])
	subprocess.check_call(args)


def write_riff_file(riff_buffer, out_file_path):
	"""Given a raw riff_buffer from a bank, outputs it in a usable format to out_file_path (without extension)"""
	f_type = riff_buffer[0:4]
	if riff_buffer[0:4] == b"RIFF":
		fmt = struct.unpack("<h", riff_buffer[20:22])[0]
		if fmt == -1:
			with open(out_file_path + ".wem", "wb") as f:
				f.write(riff_buffer)
			return wem_to_ogg(out_file_path + ".wem", out_file_path)
		elif fmt == -2:
			wav_file_path = out_file_path + ".wav"
			with open(wav_file_path, "wb") as f:
				# header up for the format chunk
				f.write(riff_buffer[:20])
				# wav, stereo
				f.write(struct.pack("<hh", 1, 2))
				# the rest
				f.write(riff_buffer[24:])
			print(wav_file_path)
			return wav_file_path
		# 2 == JUNK, not sure if readable
		else:
			logging.warning(f"Unknown RIFF format {fmt} in {out_file_path}! Please report to the devs!")
	else:
		logging.warning(f"Unknown resource format {f_type} in {out_file_path}! Please report to the devs!")


def bin_to_lua(bin_file):
	try:
		out_file = os.path.splitext(bin_file)[0]
		# out_file = os.path.join(out_dir, out_name)
		function_string = f'"{luadec}" "{bin_file}"'
		output = subprocess.Popen(function_string, stdout=subprocess.PIPE).communicate()[0]
		function_string2 = f'"{luadec}" -s "{bin_file}"'
		output2 = subprocess.Popen(function_string2, stdout=subprocess.PIPE).communicate()[0]
		# print(function_string, output)
		if len(bytearray(output)) > 0:
			with open(out_file, 'wb') as outfile:
				outfile.write(bytearray(output))
				return True
		elif len(bytearray(output2)) > 0:
			with open(out_file, 'wb') as outfile:
				outfile.write(bytearray(output2))
				return True
		else:
			print("decompile failed, skipping...")

	except subprocess.CalledProcessError as err:
		print(err)


def wem_to_ogg(wem_file, out_file):
	try:
		output = out_file + ".ogg"
		run_smart([ww2ogg, wem_file, "-o", output, "--pcb", pcb, ])
		run_smart([revorb, output])
		return output
	except subprocess.CalledProcessError as err:
		# Input: C:\Users\arnfi\AppData\Local\Temp\tmp_e_wg2dg-cobra-dds\buildings_media_B06CD10C.wem
		# Parse error: RIFF truncated
		logging.warning(err)


def dds_to_png(dds_file_path, height):
	"""Converts a DDS file given by a path to a PNG file"""
	out_dir, in_name = os.path.split(dds_file_path)
	name = os.path.splitext(in_name)[0]
	# print("dds to png", dds_file_path, out_dir, height)
	run_smart([
		BINARY, "-y", "-ft", "png", "-o", out_dir, "-f", "R8G8B8A8_UNORM", "-fl", "12.1", "-h", str(height), "-srgb",
		"-dx10", dds_file_path])
	return os.path.join(out_dir, name + '.png')


def png_to_dds(png_file_path, height, out_dir, codec="BC7_UNORM", mips=1):
	"""Converts a PNG file given by a path to a DDS file"""
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	name = os.path.splitext(in_name)[0]
	run_smart([
		BINARY, "-y", "-ft", "dds", "-o", out_dir, "-f", codec, "-fl", "12.1", "-h", str(height), "-if", "BOX",
		"-dx10", "-m", str(mips), "-srgb", "-sepalpha", "-alpha", png_file_path])
	return os.path.join(out_dir, name + '.dds')

