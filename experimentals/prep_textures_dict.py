from constants import ConstantsProvider
from ovl_util.imarray import get_split_mode

game = "Planet Zoo"
constants = ConstantsProvider(("shaders", "textures"))
shaders = constants[game]["shaders"]

all_tex = {}
for shader_name, (textures, attributes) in shaders.items():
	# print(shader_name)
	for tex in textures:
		res = get_split_mode(tex.lower(), "any_compression")
		if res:
			channels = res.split("_")
		else:
			channels = ("",)
		all_tex[tex] = channels
		# print(tex, channels)
for k, vs in sorted(all_tex.items()):
	infix = ", ".join(f'"": "{v}"' for v in vs)
	dic = {"": infix}
	s = f"# '{k}': {{{infix}}},"
	# print(k, v)
	print(s)
