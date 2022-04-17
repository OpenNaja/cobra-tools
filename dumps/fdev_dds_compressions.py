from generated.formats.dds.enum.DxgiFormat import DxgiFormat

rules = (
	("BC6_", "BC6H_"),
)

suffixes = (
	("F", "_FLOAT"),
	("U", "_UINT"),
	("UN", "_UNORM"),
	("S", "_SINT"),
	("SN", "_SNORM"),
	("UN_SRGB", "_UNORM_SRGB"),
)


dds_keys = [k.name for k in DxgiFormat]
print(dds_keys)
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
					if "BC4" in dds or "BC5" in dds or "BC6" in dds:
						pass
					else:
						if dds.endswith("_SRGB"):
							dds = dds.rstrip("_SRGB") + "_UNORM_SRGB"
						else:
							dds = dds + "_UNORM"


					# if dds.startswith("BC7"):
					# 	# BC7_UNORM, BC7_UNORM_SRGB
					# 	pass
					# # else:
					# # 	if "_S" or "_SNORM" in dds:
					# # 		pass
				else:
					for suffa, suffb in suffixes:
						if dds.endswith(suffa):
							dds = dds.rstrip(suffa) + suffb

				infix = ""
				if dds not in dds_keys:
					infix = 'custom="True" '
				result = f'<option value="{ind}" name="{dds}" {infix}/>'
				print(result)
