from generated.formats.ms2.bitfields.ModelFlag import ModelFlag

flags_1uv = (517, 528, 545, )
flags_8uv = (512, )
flags_2uv = (533, 565, 821, 853, 885, 1013)

pz_all = (512, 513, 517, 528, 529, 533, 545, 549, 565, 821, 853, 885, 1013)
# for v in flags_1uv+flags_2uv+flags_8uv:
for v in pz_all:
	f = ModelFlag.from_value(v)
	print(f)
