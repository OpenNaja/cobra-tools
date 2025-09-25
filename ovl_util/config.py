import json
import logging
import os


class BaseSetting(object):

	def __init__(self, name, tooltip, default: object = 0, options=(), accept_filter=lambda x: True):
		self.name, = name,
		self.tooltip = tooltip
		self.default = default
		self.options = options
		self.options_map = {str(option): option for option in options}
		self.accept_filter = accept_filter

	def __repr__(self):
		return f"'{self.name}' ({self.__class__.__name__}) default={self.default}, options={self.options}"

	def update(self, cfg_dict, k, v):
		# go back to the original type if it existed in options
		v = self.options_map.get(v, v)
		# print(f"setting cfg[{k}]={v} ({type(v).__name__})")
		# setattr(cfg, k, v)
		cfg_dict[k] = v


class RestartSetting(BaseSetting):
	def __init__(self, name, tooltip, default: object = 0, options=(), accept_filter=lambda x: True):
		super().__init__(name, tooltip, default, options, accept_filter)
		if self.tooltip:
			self.tooltip += " - needs restart"


class ImmediateSetting(BaseSetting):
	pass


class DeferredSetting(BaseSetting):
	pass


class TransientSetting(BaseSetting):
	pass


class Config(dict):

	# recent_ovls = ImmediateSetting("Recent OVLs", "The last OVL files that have been accessed", [])
	# current_ovl = TransientSetting("Current OVL", "The last OVL file that has been accessed", "some_ovl.ovl", (), lambda x: x.endswith(".ovl"))
	oodle_level = TransientSetting("Oodle Level", "Higher numbers compress better, while lower numbers compress faster", 6, list(range(10)))
	debug_mode = TransientSetting("Debug Mode", "Enables debugging when checked:\n"
												" - OVLs open slower to verify structs don't miss pointers\n"
												" - temporary files are kept in extract folder\n"
												" - debug info is added to XML-like extracts", False, (True, False))
	# DDS settings
	dds_use_gpu = TransientSetting("Use GPU Compression", "GPU is faster but less accurate, especially on MIP maps", True, (True, False))
	# dds_quality = TransientSetting("Compressonator Quality", "Compression quality when using Compressonator", 0, (0, 1))  # todo
	dds_extract = TransientSetting("Keep DDS", "Keep DDS files in extraction", False, (True, False))
	lua_decompile = TransientSetting("Decompile LUA", "Try to decompile LUA; does not always work and slows down full extractions", True, (True, False))
	lua_flatten = TransientSetting("Flatten LUA subfolders", "Flatten LUA filenames that are in subfolders on injection and unflatten into folders on extraction", False, (True, False))
	motiongraph_rename_sound = TransientSetting("Replace sounds in MOTIONGRAPH", "Rename references to sound events during rename contents. Make sure to refer to existing events only", False, (True, False))
	update_aux = TransientSetting("Rewrite AUX files", "Rewrite AUX files when saving the OVL", True, (True, False))
	play_on_saving = TransientSetting("Run Game on Saving", "Always run the currently selected game after saving an OVL", False, (True, False))
	# GUI appearance
	enable_logger_widget = RestartSetting("Enable Logger", "Enable Logger widget in GUI", True, (True, False))
	logger_orientation = RestartSetting("Logger Orientation", "Set logger orientation", "H", ("H", "V"))
	theme = RestartSetting("Theme", "Select theme palette", "dark", ("dark", "light"))
	num_recent = TransientSetting("Number of recent files", "Number of files to show in 'Open Recent' dialogues",
								   5, list(range(3, 10)))
	# Editors
	preferred_editor = TransientSetting("Editor", "Preferred IDE/editor", "VS Code", ("VS Code", "PyCharm"))

	def __init__(self, dir, name="config.json", **kwargs):
		super().__init__(**kwargs)
		self.dir = dir
		self.name = name

	@property
	def settings(self):
		return {k: v for k, v in self.__class__.__dict__.items() if isinstance(v, BaseSetting)}

	@property
	def cfg_path(self):
		return os.path.join(self.dir, self.name)

	def save(self):
		logging.debug(f"Saving config")
		try:
			with open(self.cfg_path, "w") as json_writer:
				json.dump(self, json_writer, indent="\t", sort_keys=True)
		except:
			logging.exception(f"Saving '{self.cfg_path}' failed")

	def load(self):
		# populate cfg with defaults from managers, so that these make it to disk on saving
		for k, v in self.settings.items():
			self[k] = v.default
		# then try to read any that are stored
		try:
			with open(self.cfg_path, "r") as json_reader:
				from_json = json.load(json_reader)
				self.update(from_json)
				return
		except FileNotFoundError:
			logging.debug(f"Config file missing at {self.cfg_path}")
		except json.decoder.JSONDecodeError as e:
			logging.error(f"Config file broken at {self.cfg_path}")
			logging.error(str(e))


def save_config(cfg_path, cfg_dict):
	logging.info(f"Saving config to {cfg_path}")
	with open(cfg_path, "w") as json_writer:
		json.dump(cfg_dict, json_writer, indent="\t", sort_keys=True)


def load_config(cfg_path):
	try:
		logging.info(f"Loading config from {cfg_path}")
		with open(cfg_path, "r") as json_reader:
			return json.load(json_reader)
	except FileNotFoundError:
		logging.debug(f"Config file missing at {cfg_path}")
		return {}
	except json.decoder.JSONDecodeError as e:
		logging.error(f"Config file broken at {cfg_path}")
		logging.error(str(e))
		return {}


def read_str_dict(cfg_path):
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


def write_str_dict(cfg_path, config_dict):
	stream = "\n".join([key + "=" + str(val) for key, val in config_dict.items()])
	with open(cfg_path, 'w', encoding='utf8') as cfg_file:
		cfg_file.write(stream)


def read_list(cfg_path):
	try:
		with open(cfg_path, 'r', encoding='utf-8') as cfg_file:
			return [line.strip() for line in cfg_file if line.strip() and not line.startswith("#")]
	except:
		print(f"{cfg_path} is missing or broken!")
		return []
