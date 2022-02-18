import logging
import sys
import os

plugin_dir = os.path.dirname(os.path.dirname(__file__))


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


def logging_setup(log_name):
	log_path = f'{os.path.join(plugin_dir, log_name)}.log'
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
	formatter = logging.Formatter('%(levelname)s | %(message)s')
	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.INFO)
	stdout_handler.setFormatter(formatter)
	file_handler = logging.FileHandler(log_path, mode="w")
	file_handler.setLevel(logging.DEBUG)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.addHandler(stdout_handler)


def get_version():
	init_path = f'{os.path.join(plugin_dir, "__init__")}.py'
	with open(init_path, "r") as f:
		line = ""
		while '"version"' not in line:
			line = f.readline()
		# 	"version": (2, 3, 1),
		_, r = line.split("(", 1)
		version_raw, _ = r.split(")", 1)
		version = [int(x.strip()) for x in version_raw.split(",")]
	return version


def get_version_str():
	version_tuple = get_version()
	return '.'.join([str(x) for x in version_tuple])


def get_commit_str():
	with open(os.path.join(plugin_dir, "version.txt"), "r") as f:
		return f.read()


if __name__ == '__main__':
	cfg = read_config("config.ini")
	print(cfg)
