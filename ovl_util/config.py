
def read_config(cfg_path):
	config_dict = {}
	try:
		with open(cfg_path, 'r', encoding='utf-8') as cfg_file:
			for line in cfg_file:
				if not line.startswith("#") and "=" in line:
					(key, val) = line.strip().split("=")
					key = key.strip()
					val = val.strip()
					if val.startswith("["):
						# strip list format [' ... ']
						val = val[2:-2]
						config_dict[key] = [v.strip() for v in val.split("', '")]
					else:
						config_dict[key] = val
	except:
		print(f"{cfg_path} is missing or broken!")
	return config_dict


def write_config(cfg_path, config_dict):
	stream = "\n".join([key+"="+str(val) for key, val in config_dict.items()])
	with open(cfg_path, 'w', encoding='utf8') as cfg_file:
		cfg_file.write(stream)


def read_list(cfg_path):
	try:
		with open(cfg_path, 'r', encoding='utf-8') as cfg_file:
			return [line.strip() for line in cfg_file if line.strip() and not line.startswith("#")]
	except:
		print(f"{cfg_path} is missing or broken!")
		return []


if __name__ == '__main__':
	cfg = read_config("config.ini")
	print(cfg)
