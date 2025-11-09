import logging
import os
import re
import subprocess
import struct
import sys

from utils.shared import check_any

util_dir = os.path.dirname(__file__)
BINARY = os.path.normpath(os.path.join(util_dir, "texconv/texconv.exe"))
ww2ogg = os.path.normpath(os.path.join(util_dir, "ww2ogg/ww2ogg.exe"))
pcb = os.path.normpath(os.path.join(util_dir, "ww2ogg/packed_codebooks_aoTuV_603.bin"))
revorb = os.path.normpath(os.path.join(util_dir, "revorb/revorb.exe"))
luadec = os.path.normpath(os.path.join(util_dir, "luadec/luadec.exe"))
luacheck = os.path.normpath(os.path.join(util_dir, "luacheck/luacheck.exe"))

DECOMPILE_TIMEOUT = 10
PREFAB_ROOT = b"l_0_2"

BYTE_REPLACEMENTS_PREFAB = [
	# Replacements for Prefab Lua specifically
	# Example: b'= .setmetatable' -> b'= setmetatable'
	(br'(=\s*)\.\s*(setmetatable|_G)\b', br'\1\2'),
	# Example: b'(.require)' -> b'require'
	(br'\(\s*\.\s*(module|require|math)\s*\)', br'\1'),
	# Example: b'.Root' -> b'l_0_2.Root'
	(br'\.(FlattenedRoot|Root|GetRoot|GetFlattenedRoot)\b', br'l_0_2.\1'),
]

BYTE_REPLACEMENTS = [
	# Syntax Errors from custom Lua
	# < 0, 0, 0 > -> vec3_const(0, 0, 0)
	(
		br'<\s*?([0-9\-\.]+(?:e[+-]?[0-9]+)?)\s*?,\s*?([0-9\-\.]+(?:e[+-]?[0-9]+)?)\s*?,\s*?([0-9\-\.]+(?:e[+-]?[0-9]+)?)\s*?>',
		br'vec3_const(\1, \2, \3)'
	),
	(br'\s\.end\b', br' nil'),
]

COMPILED_BYTE_REPLACEMENTS = [
	(re.compile(pattern), replacement) for pattern, replacement in BYTE_REPLACEMENTS
]

COMPILED_BYTE_REPLACEMENTS_PREFAB = [
	(re.compile(pattern), replacement) for pattern, replacement in BYTE_REPLACEMENTS_PREFAB
]

def sanitize_lua_content(content: bytes) -> bytes:
	"""
	Performs a series of regex replacements on the raw Lua content
	to fix custom syntax
	"""
	if PREFAB_ROOT in content:
		for compiled_pattern, replacement in COMPILED_BYTE_REPLACEMENTS_PREFAB:
			content = compiled_pattern.sub(replacement, content)

	for compiled_pattern, replacement in COMPILED_BYTE_REPLACEMENTS:
		content = compiled_pattern.sub(replacement, content)
	
	return content

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


def bin_to_lua(bin_path) -> tuple[bytes, str] | tuple[None, str] | tuple[None, None]:
	file_name = os.path.basename(bin_path)
	for call_sig in (f'"{luadec}" "{bin_path}"', f'"{luadec}" -s "{bin_path}"'):
		try:
			proc = subprocess.Popen(call_sig, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = proc.communicate(timeout=DECOMPILE_TIMEOUT)
			err_msg = err.decode(errors='ignore').strip()
			if output:
				# If there was also a message on stderr, log it as a warning
				if err_msg:
					logging.warning(f"Decompiler warnings for {file_name}", extra={"details": err_msg})
				return sanitize_lua_content(output), err_msg
			# The decompiler produced no output, but printed an error message
			elif err_msg:
				logging.error(f"Decompiling {file_name} failed with errors", extra={"details": err_msg})
				return None, err_msg
		except subprocess.TimeoutExpired:
			# Kill long luadec processes to recover from bad files
			proc.kill()
			output, err = proc.communicate()
			err_msg = err.decode(errors='ignore').strip()
			log_message = f"Decompiling {file_name} timed out after {DECOMPILE_TIMEOUT} seconds."
			logging.error(log_message, extra={"details": err_msg})
			return None, err_msg
		except Exception:
			logging.exception(f"Decompiling {file_name} failed with an unexpected error.")
			return None, None

	logging.error(f"Decompiling {file_name} returned no result.")
	return None, None


error_code_filters: dict[int, tuple[str, ...]] = {
	113: ("vec3_const", "vec2_const"),
}


def filter_error_code(error_code: int, msg: str) -> bool:
	filters: tuple[str, ...] = error_code_filters.get(error_code, ())
	return check_any(filters, msg)


def check_lua_syntax(lua_path):
	try:
		# https://luacheck.readthedocs.io/en/stable/cli.html
		# https://luacheck.readthedocs.io/en/stable/warnings.html
		# https://stackoverflow.com/questions/49158143/how-to-ignore-luacheck-warnings
		function_string = f'"{luacheck}" "{lua_path}" --codes'
		lua_name = os.path.basename(lua_path)
		# capture the console output
		bytes_output = subprocess.Popen(function_string, stdout=subprocess.PIPE).communicate()[0]
		# luacheck doesn't seem to handle non-ASCII chars when printing lua_path, so just escape them
		output = bytes_output.decode(sys.getdefaultencoding(), errors="surrogateescape")
		lines = [line.strip() for line in output.split("\r\n")]
		for line in lines:
			if line.startswith(lua_path):
				line_nr, col_nr, info = line.replace(lua_path + ":", "").split(":", 3)
				match = re.search(r"[EW][0-9]+", info, flags=0)
				error_code = int(match.group(0).lstrip("EW"))
				msg = f"{lua_name}: line {line_nr}, column {col_nr}: {info.strip()}"
				# select which luacheck warnings to show to user
				if filter_error_code(error_code, msg):
					continue
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


def dds_to_png(dds_file_path, codec):
	"""Converts a DDS file given by a path to a PNG file"""
	out_dir, in_name = os.path.split(dds_file_path)
	name = os.path.splitext(in_name)[0]
	args = [BINARY, "-y", "-ft", "png", "-o", out_dir, "-fl", "12.1", "-dx10"]
	# logging.info(f"Selective SRGB {codec}")
	if "SRGB" in codec:
		args.extend(("-f", "R8G8B8A8_UNORM_SRGB", "-srgb"))
	else:
		args.extend(("-f", "R8G8B8A8_UNORM"))
	args.append(dds_file_path)
	run_smart(args)
	return os.path.join(out_dir, name + '.png')


def png_to_dds(png_file_path, out_dir, codec="BC7_UNORM", num_mips=0, dds_use_gpu=False):
	"""Converts a PNG file given by a path to a DDS file"""
	png_file_path = os.path.normpath(png_file_path)
	in_dir, in_name = os.path.split(png_file_path)
	name = os.path.splitext(in_name)[0]
	args = [BINARY, "-y", "-ft", "dds", "-o", out_dir, "-f", codec, "-fl", "12.1", "-if", "FANT_DITHER_DIFFUSION",
		"-dx10", "-m", str(num_mips), "-sepalpha"]
	if "SRGB" in codec:
		args.append("-srgb")
	if not dds_use_gpu:
		args.append("-nogpu")
	args.append(png_file_path)
	run_smart(args)
	return os.path.join(out_dir, name + '.dds')
