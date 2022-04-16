rules = (
	("BC6_", "BC6H_"),
)

fp = "fdev_dds_compressions.txt"
with open(fp, "r") as f:
	for l in f.readlines():
		if l:
			if "#" in l:
				left, right = l.split("#")
				res = right.split(" ")
				valid_res = [r for r in res if r.strip()]
				ind = valid_res[0]
				dds = valid_res[1].upper().replace("F3DFORMAT_", "")
				for bef, after in rules:
					dds = dds.replace(bef, after)
				if dds.startswith("BC"):
					if dds.startswith("BC7"):
						# BC7_UNORM, BC7_UNORM_SRGB
						pass
					else:
						if "_S" or "_SNORM" in dds:
							pass

				result = f'<option value="{ind}" name="{dds}" />'
				print(result)
