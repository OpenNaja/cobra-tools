import os

from constants import ConstantsProvider
from constants.converter import write_audio_dict
from modules.formats.shared import fnv1_32
from modules.walker import get_game_constants_dir

constants = ConstantsProvider()
game = "Jurassic World Evolution 2"
lut = constants[game].get("audio", {})

fp = "../dumps/fnv1_32_dump_JWE2.txt"

with open(fp) as f:
	for line in f.readlines():
		line = line.strip()
		h = fnv1_32(line.lower().encode())
		lut[h] = line
print(lut)
out_dir = get_game_constants_dir(game)
print(out_dir)
os.makedirs(out_dir, exist_ok=True)
write_audio_dict(os.path.join(out_dir, "audio.py"), lut)