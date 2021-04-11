import os


def increment_strip(fp, increment=5):
	bp, ext = os.path.splitext(fp)
	with open(fp, "rb") as f:
		d = f.read()

	for i in range(increment):

		with open(f"{bp}_{i}_strip{ext}", "wb") as fo:
			fo.write(d[i:].rstrip(b"x\00"))
		with open(f"{bp}_{i}{ext}", "wb") as fo:
			fo.write(d[i:])


increment_strip("C:/Users/arnfi/Desktop/Coding/ovl/OVLs/anim test/rot_x_0_22_42_def_c_new_end.maniskeys", increment=5)
