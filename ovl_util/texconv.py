import logging
import os
import re
import subprocess
import struct

util_dir = os.path.dirname(__file__)
BINARY = os.path.normpath(os.path.join(util_dir, "texconv/texconv.exe"))
ww2ogg = os.path.normpath(os.path.join(util_dir, "ww2ogg/ww2ogg.exe"))
pcb = os.path.normpath(os.path.join(util_dir, "ww2ogg/packed_codebooks_aoTuV_603.bin"))
revorb = os.path.normpath(os.path.join(util_dir, "revorb/revorb.exe"))
luadec = os.path.normpath(os.path.join(util_dir, "luadec/luadec.exe"))
luacheck = os.path.normpath(os.path.join(util_dir, "luacheck/luacheck.exe"))


def run_smart(args):
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


def check_lua_syntax(lua_path):
	try:
		# https://luacheck.readthedocs.io/en/stable/cli.html
		# https://luacheck.readthedocs.io/en/stable/warnings.html
		# https://stackoverflow.com/questions/49158143/how-to-ignore-luacheck-warnings
		function_string = f'"{luacheck}" "{lua_path}" --codes'
		lua_name = os.path.basename(lua_path)
		# capture the console output
		bytes_output = subprocess.Popen(function_string, stdout=subprocess.PIPE).communicate()[0]
		output = bytes_output.decode()
		lines = [line.strip() for line in output.split("\r\n")]
		for line in lines:
			if line.startswith(lua_path):
				line_nr, col_nr, info = line.replace(lua_path + ":", "").split(":", 3)
				match = re.search(r"[EW][0-9]+", info, flags=0)
				error_code = int(match.group(0).lstrip("EW"))
				msg = f"{lua_name}: line {line_nr}, column {col_nr}: {info.strip()}"
				# select which luacheck warnings to show to user
				if error_code < 100:
					raise SyntaxError(msg)
				elif 100 <= error_code < 200:
					logging.warning(msg)
				elif 200 <= error_code < 400:
					logging.debug(msg)
				elif 400 <= error_code < 600:
					logging.warning(msg)
				else:
					logging.debug(msg)
	except subprocess.CalledProcessError:
		logging.exception(f"Something went wrong")


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


def dds_to_png(dds_file_path):
	"""Converts a DDS file given by a path to a PNG file"""
	out_dir, in_name = os.path.split(dds_file_path)
	name = os.path.splitext(in_name)[0]
	run_smart([
		BINARY, "-y", "-ft", "png", "-o", out_dir, "-f", "R8G8B8A8_UNORM", "-fl", "12.1", "-srgb",
		"-dx10", dds_file_path])
	return os.path.join(out_dir, name + '.png')


def png_to_dds(png_file_path, out_dir, codec="BC7_UNORM", mips=0):
	"""Converts a PNG file given by a path to a DDS file"""
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	name = os.path.splitext(in_name)[0]
	run_smart([
		BINARY, "-l", "-y", "-ft", "dds", "-o", out_dir, "-f", codec, "-fl", "12.1", "-if", "FANT_DITHER_DIFFUSION",
		"-dx10", "-m", str(mips), "-srgb", "-sepalpha", "-alpha", png_file_path])
	return os.path.join(out_dir, name + '.dds')


def png_to_uncompressed_dds(png_file_path, height, out_dir, codec="BC7_UNORM"):
	"""Converts a PNG file given by a path to a DDS file"""
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	name = os.path.splitext(in_name)[0]
	run_smart([
		# BINARY, "-l", "-y", "-ft", "dds", "-o", out_dir, "-f", "R8G8B8A8_UNORM", "-fl", "12.1", "-h", str(height), "-if", "BOX",
		BINARY, "-l", "-y", "-ft", "dds", "-o", out_dir, "-f", codec, "-fl", "12.1", "-h", str(height), "-if", "FANT_DITHER_DIFFUSION",
		"-dx10", "-m", "1", "-srgb", "-sepalpha", "-alpha", png_file_path])
	return os.path.join(out_dir, name + '.dds')


def add_mips_to_dds(dds_file_path, out_dir, codec="BC7_UNORM", mips=0):
	"""Converts a PNG file given by a path to a DDS file"""
	dds_file_path = os.path.normpath(dds_file_path)
	in_dir, in_name = os.path.split(dds_file_path)
	exp_dir = os.path.join(out_dir, "mips")
	os.makedirs(exp_dir, exist_ok=True)
	with_mips = os.path.join(exp_dir, in_name)
	run_smart([
		BINARY, "-l", "-y", "-ft", "dds", "-o", exp_dir, "-f", codec, "-fl", "12.1", "-if", "FANT_DITHER_DIFFUSION",
		"-dx10", "-m", str(mips), "-srgb", "-sepalpha", "-alpha", dds_file_path])
	return with_mips

