from constants import ConstantsProvider
from ovl_util.imarray import get_split_mode

# game = "Planet Zoo"
# game = "Jurassic World Evolution 2"
game = "Planet Coaster"
game = "Jurassic World Evolution 3"
constants = ConstantsProvider(("shaders", "textures"))
shaders = constants[game]["shaders"]

all_tex = {}
for shader_name, (textures, attributes) in shaders.items():
	# print(shader_name)
	for tex in textures:
		res = get_split_mode(None, tex.lower(), "any_compression")
		if res:
			channels = res.split("_")
		else:
			channels = ("",)
		all_tex[tex] = channels
		# print(tex, channels)
	# if any(t.endswith("2") for t in textures):
	# 	print("has suffix2")
	# 	print(shader_name)
	# 	print(textures)
for k, vs in sorted(all_tex.items()):
	infix = ", ".join(f'"{v}": ""' for v in vs)
	dic = {"": infix}
	s = f"# '{k}': {{{infix}}},"
	# print(k, v)
	print(s)

# store in constants folder
# then, populate it manually using the shorthand codes defined in \plugin\utils\texture_settings.py
