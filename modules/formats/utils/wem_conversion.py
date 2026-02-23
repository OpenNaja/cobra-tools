import logging
import os
import struct
import subprocess

from modules.formats.utils import util_dir, check_call_smart

ww2ogg = os.path.normpath(os.path.join(util_dir, "ww2ogg/ww2ogg.exe"))
pcb = os.path.normpath(os.path.join(util_dir, "ww2ogg/packed_codebooks_aoTuV_603.bin"))
revorb = os.path.normpath(os.path.join(util_dir, "revorb/revorb.exe"))


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


def wem_to_ogg(wem_file, out_file):
	try:
		output = out_file + ".ogg"
		check_call_smart([ww2ogg, wem_file, "-o", output, "--pcb", pcb, ])
		check_call_smart([revorb, output])
		return output
	except subprocess.CalledProcessError as err:
		# Input: C:\Users\arnfi\AppData\Local\Temp\tmp_e_wg2dg-cobra-dds\buildings_media_B06CD10C.wem
		# Parse error: RIFF truncated
		logging.warning(err)
