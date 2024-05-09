import json
import logging
import os

from root_path import root_dir


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
		print(f"setting cfg[{k}]={v}")
		# go back to the original type
		v = self.options_map.get(v, v)
		# setattr(cfg, k, v)
		cfg_dict[k] = v

	# def __get__(self, instance, owner):
	# 	print("__get__", instance, owner)
	# 	return self

	# def __set__(self, instance, value):
	# 	print("__set__", instance, value)
	# 	setattr(instance, self.name, value)


class ImmediateSetting(BaseSetting):
	pass


class DeferredSetting(BaseSetting):
	pass


class TransientSetting(BaseSetting):
	pass


class Config(dict):

	# immediate = ("recent_ovls", )
	recent_ovls = ImmediateSetting("Recent OVLs", "The last OVL files that have been accessed", [])
	current_ovl = TransientSetting("Current OVL", "The last OVL file that has been accessed", "some_ovl.ovl", (), lambda x: x.endswith(".ovl"))
	oodle_level = TransientSetting("Oodle Level", "Higher numbers compress better, while lower numbers compress faster", 6, list(range(10)))
	# DDS settings
	dds_use_gpu = TransientSetting("Use GPU Compression", "GPU is faster but less accurate, especially on MIP maps", True, (True, False))
	# dds_quality = TransientSetting("Compressonator Quality", "Compression quality when using Compressonator", 0, (0, 1))  # todo
	dds_extract = TransientSetting("Keep DDS", "Keep DDS files in extraction", False, (True, False))
	show_logger = ImmediateSetting("Show Logger", "Show Logger widget - needs restart", False, (True, False))
	name = "config.json"

	def __setitem__(self, k, v):
		super().__setitem__(k, v)
		# key for manager may not exist
		manager = self.settings.get(k)
		if manager and isinstance(manager, ImmediateSetting):
			logging.info(f"Saved '{self.name}' after storing '{k}'")
			self.save()
	#
	# def __getitem__(self, k):
	# 	return self[k]

	def __init__(self, name="config.json", **kwargs):
		super().__init__(**kwargs)
		self.name = name

	@property
	def settings(self):
		# print(self.__members__)
		members = {k: v for k, v in self.__class__.__dict__.items() if isinstance(v, BaseSetting)}
		# print("dict", )
		# sets = {"recent_ovls": self.recent_ovls}
		return members
		# return self.__annotations__
		# total_members = []
		# for key, value in dict.items():
		# 	if isinstance(value, BitfieldMember):
		# 		total_members.append(key)
		# cls.__members__ = total_members

	@property
	def cfg_path(self):
		return os.path.join(root_dir, self.name)

	def save(self):
		logging.info(f"Saving config")
		try:
			with open(self.cfg_path, "w") as json_writer:
				json.dump(self, json_writer, indent="\t", sort_keys=True)
				# json.dump(self.__slots__, json_writer, indent="\t", sort_keys=True)
		except:
			logging.exception(f"Saving '{self.cfg_path}' failed")

	def load(self):
		try:
			with open(self.cfg_path, "r") as json_reader:
				self.update(json.load(json_reader))
		except FileNotFoundError:
			logging.debug(f"Config file missing at {self.cfg_path}")
		except json.decoder.JSONDecodeError as e:
			logging.error(f"Config file broken at {self.cfg_path}")
			logging.error(str(e))


def save_config(cfg_dict):
	logging.info(f"Saving config")
	with open(os.path.join(root_dir, "config.json"), "w") as json_writer:
		json.dump(cfg_dict, json_writer, indent="\t", sort_keys=True)


def load_config():
	try:
		cfg_path = os.path.join(root_dir, 'config.json')
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


if __name__ == '__main__':
	cfg = Config()
	cfg.load()
	print(cfg)
	# print(cfg.settings)
	import sys
	from gui.widgets import LabelCombo
	from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication


	class Window(QWidget):

		def __init__(self):
			super().__init__()

			self.vlayout = QVBoxLayout()
			# remove_layout.clicked.connect(self.remove_layout)
			for cfg_key, cfg_manager in cfg.settings.items():
				def make_setter():
					cfg_key2 = str(cfg_key)
					# print(cfg_key)
					def set_key(v):
						# nonlocal cfg_key
						print(cfg_key2)
						cfg_manager.update(cfg, cfg_key2, v)
						# setattr(cfg, cfg_key, v)
					return set_key
				set_key = make_setter()
				c = LabelCombo(cfg_manager.name, [str(x) for x in cfg_manager.options], editable=not bool(cfg_manager.options), activated_fn=set_key)
				c.entry.setText(str(cfg.get(cfg_key, cfg_manager.default)))
				self.vlayout.addWidget(c)
			self.setLayout(self.vlayout)

	app = QApplication(sys.argv)

	w = Window()
	w.show()

	app.exec()
	print(cfg)
	# c.show()
