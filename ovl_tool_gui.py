import os
import struct
import sys
import time
import traceback

import modules.formats.shared
import util.interaction

try:
	from PyQt5 import QtWidgets
	import numpy as np
	import binascii

	from util import widgets
	from modules import extract, inject, hasher, walker
	from generated.formats.ovl import OvlFile
	from generated.formats.ms2 import Mdl2File
except Exception as err:
	traceback.print_exc()
	time.sleep(15)


def to_hex_str(uint):
	return binascii.hexlify(struct.pack("I", uint)).upper().decode()


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Tool", )
		self.resize(720, 400)

		self.ovl_data = OvlFile(progress_callback=self.update_progress)

		supported_types = ("DDS", "PNG", "MDL2", "TXT", "FGM", "FDB", "MATCOL", "XMLCONFIG", "ASSETPKG", "LUA", "WEM", "OTF", "TTF")
		self.filter = "Supported files ({})".format(" ".join("*."+t for t in supported_types))

		self.file_widget = widgets.FileWidget(self, self.cfg)
		self.file_widget.setToolTip("The name of the OVL file that is currently open.")

		self.p_action = QtWidgets.QProgressBar(self)
		self.p_action.setGeometry(0, 0, 200, 15)
		self.p_action.setTextVisible(True)
		self.p_action.setMaximum(1)
		self.p_action.setValue(0)
		self.t_action_current_message = "No operation in progress"
		self.t_action = QtWidgets.QLabel(self, text=self.t_action_current_message)

		header_names = ["Name", "File Type", "DJB", "Unk0", "Unk1"]
		self.table = widgets.SortableTable(header_names, self)
		# toggles
		self.t_show_temp_files = QtWidgets.QCheckBox("Save Temp Files")
		self.t_show_temp_files.setToolTip("By default, temporary files are converted to usable ones and back on the fly.")
		self.t_show_temp_files.setChecked(False)

		self.t_2K = QtWidgets.QCheckBox("Inject 2K")
		self.t_2K.setToolTip("Experimental: Increase a JWE Diffuse or Normal map to 2048x2048 resolution.")
		self.t_2K.setChecked(False)

		self.ext_dat = QtWidgets.QCheckBox("Use External Dat")
		self.ext_dat.setToolTip("Experimental: Save the ovl with an external STATIC Dat instead of one in memory")
		self.ext_dat.setChecked(False)
		self.ext_dat.stateChanged.connect(self.dat_show)
        
		self.dat_path = QtWidgets.QLineEdit("External .dat file path")
		self.dat_path.setToolTip("note: use / for the file path, not \\")
		self.dat_path.hide()

		self.remove = QtWidgets.QLineEdit("file to remove")

		self.e_name_pairs = [(QtWidgets.QLineEdit("old"), QtWidgets.QLineEdit("new"))  for i in range(1)]

		self.t_write_dat = QtWidgets.QCheckBox("Save DAT")
		self.t_write_dat.setToolTip("Writes decompressed archive streams to DAT files for debugging.")
		self.t_write_dat.setChecked(False)
		self.t_write_dat.stateChanged.connect(self.load)

		self.t_write_frag_log = QtWidgets.QCheckBox("Save Frag Log")
		self.t_write_frag_log.setToolTip("For devs.")
		self.t_write_frag_log.setChecked(False)
		self.t_write_frag_log.stateChanged.connect(self.load)

		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0, 1, 8)
		self.qgrid.addWidget(self.t_show_temp_files, 1, 0)
		self.qgrid.addWidget(self.t_write_dat, 1, 1)
		self.qgrid.addWidget(self.t_write_frag_log, 1, 2)
		self.qgrid.addWidget(self.t_2K, 1, 3)
		self.qgrid.addWidget(self.ext_dat, 1, 4)
		for (old, new) in self.e_name_pairs:
			self.qgrid.addWidget(old, 1, 5)
			self.qgrid.addWidget(new, 1, 6)
		self.qgrid.addWidget(self.remove, 1, 7)
		self.qgrid.addWidget(self.table, 2, 0, 1, 8)
		self.qgrid.addWidget(self.p_action, 3, 0, 1, 8)
		self.qgrid.addWidget(self.t_action, 4, 0, 1, 8)
		self.qgrid.addWidget(self.dat_path, 5,0,1,8)
		self.central_widget.setLayout(self.qgrid)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('File')
		editMenu = mainMenu.addMenu('Edit')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ((fileMenu, "Open", self.file_widget.ask_open, "CTRL+O", "dir"),
					   (fileMenu, "Save", self.save_ovl, "CTRL+S", "save"),
					   (fileMenu, "Exit", self.close, "", "exit"),
					   (editMenu, "Unpack", self.extract_all, "CTRL+U", "extract"),
					   (editMenu, "Inject", self.inject, "CTRL+I", "inject"),
					   (editMenu, "Hash", self.hasher, "CTRL+H", ""),
					   (editMenu, "Remove", self.remover, "CTRL+R", ""),
					   (editMenu, "Walk", self.walker, "", ""),
					   (editMenu, "Generate Hash Table", self.walker_hash, "", ""),
					   (helpMenu, "Report Bug", self.report_bug, "", "report"),
					   (helpMenu, "Documentation", self.online_support, "", "manual"))
		self.add_to_menu(button_data)
		self.check_version()
		self.load_hash_table()

	@property
	def commands(self,):
		# get those commands that are set to True
		return [x for x in ("write_dat", "write_frag_log") if getattr(self, x)]

	@property
	def show_temp_files(self,):
		return self.t_show_temp_files.isChecked()

	@property
	def write_2K(self,):
		return self.t_2K.isChecked()
	
	@property
	def use_ext_dat(self,):
		return self.ext_dat.isChecked()

	@property
	def write_dat(self,):
		return self.t_write_dat.isChecked()

	@property
	def write_frag_log(self,):
		return self.t_write_frag_log.isChecked()
	
	def dat_show(self,):
		if self.use_ext_dat == True:
			self.dat_path.show()
		else:
			self.dat_path.hide()

	def update_commands(self):
		# at some point, just set commands to archive and trigger changes there
		if self.file_widget.filename:
			self.ovl_data.commands = self.commands

	def update_progress(self, message, value=None, vmax=None):
		# avoid gui updates if the value won't actually change the percentage.
		# this saves us from making lots of GUI update calls that don't really
		# matter.
		try:
			if vmax > 100 and (value % (vmax // 100)) and value != 0:
				value = None
		except ZeroDivisionError:
			value = 0
		except TypeError:
			value = None

		# update progress bar values if specified
		if value is not None:
			self.p_action.setValue(value)
		if vmax is not None:
			self.p_action.setMaximum(vmax)

		# don't update the GUI unless the message has changed. label updates
		# are expensive
		if self.t_action_current_message != message:
			self.t_action.setText(message)
			self.t_action_current_message = message

	def load_hash_table(self):
		print("Loading hash table...")
		start_time = time.time()
		self.hash_table = {}
		hashes_dir = os.path.join(os.getcwd(), "hashes")
		try:
			for file in os.listdir(hashes_dir):
				if file.endswith(".txt"):
					with open(os.path.join(hashes_dir, file), "r") as f:
						for line in f:
							line = line.strip()
							if line:
								k, v = line.split(" = ")
								self.hash_table[int(k)] = v
		except:
			pass
		# print(self.hash_table)
		print(f"Loaded {len(self.hash_table)} hash - name pairs in {time.time()-start_time:.2f} seconds.")

	def load(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			self.update_progress("Reading OVL " + self.file_widget.filepath, value=0, vmax=0)
			try:
				self.ovl_data.load(self.file_widget.filepath, commands=self.commands, hash_table=self.hash_table)
			except Exception as ex:
				traceback.print_exc()
				util.interaction.showdialog(str(ex))
				print(ex)
			self.update_gui_table()

	def update_gui_table(self,):
		start_time = time.time()
		data = []
		print(f"Loading {len(self.ovl_data.files)} files into gui...")
		for file_w in self.ovl_data.files:
			name = f"{file_w.name}.{file_w.ext}"
			# line = [name, file_w.ext, to_hex_str(file_w.file_hash), str(file_w.unkn_0), str(file_w.unkn_1)]
			line = [name, file_w.ext, file_w.file_hash, file_w.unkn_0, file_w.unkn_1]
			data.append(line)
		self.table.set_data(data)
		print(f"Loaded GUI in {time.time()-start_time:.2f} seconds!")
		self.update_progress("Operation completed!", value=1, vmax=1)

	def save_ovl(self):
		if self.file_widget.filename:
			file_src = QtWidgets.QFileDialog.getSaveFileName(self, 'Save OVL', os.path.join(self.cfg.get("dir_ovls_out", "C://"), self.file_widget.filename), "OVL files (*.ovl)",)[0]
			if file_src:
				self.cfg["dir_ovls_out"], ovl_name = os.path.split(file_src)
				try:
					self.ovl_data.save(file_src, self.use_ext_dat, self.dat_path.text())
				except BaseException as error:
					print(error)
				self.file_widget.dirty = False
				print("Done!")

	def skip_messages(self, error_files, skip_files):
		error_count = len(error_files)
		skip_count = len(skip_files)
		if error_count:
			print("Files not extracted due to error:")
			for ef in error_files:
				print("\t",ef)

		if skip_count:
			print("Unsupported files not extracted:")
			for sf in skip_files:
				print("\t",sf)

		if error_count or skip_count:
			message = f"{error_count + skip_count} files were not extracted from the archive and may be missing from the output folder. {skip_count} were unsupported, while {error_count} produced errors."
			util.interaction.showdialog(message)

	def extract_all(self):
		if self.file_widget.filename:
			out_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg.get("dir_extract", "C://"), )
			if out_dir:
				self.cfg["dir_extract"] = out_dir
				# create output dir
				try:
					os.makedirs(out_dir, exist_ok=True)
					archive = self.ovl_data.ovs_files[0]
					error_files, skip_files = extract.extract(archive, out_dir, self.show_temp_files, progress_callback=self.update_progress)

					self.skip_messages(error_files, skip_files)
					self.update_progress("Operation completed!", value=1, vmax=1)
				except Exception as ex:
					traceback.print_exc()
					util.interaction.showdialog(str(ex))
					print(ex)
		else:
			util.interaction.showdialog("You must open an OVL file before you can extract files!")

	def inject(self):
		if self.file_widget.filename:
			files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Inject files', self.cfg.get("dir_inject", "C://"), self.filter)[0]
			if files:
				self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:
				inject.inject(self.ovl_data, files, self.show_temp_files, self.write_2K)
				self.file_widget.dirty = True
			except Exception as ex:
				traceback.print_exc()
				util.interaction.showdialog(str(ex))
			print("Done!")
		else:
			util.interaction.showdialog("You must open an OVL file before you can inject files!")

	def hasher(self):
		if self.file_widget.filename:
			names = [(tup[0].text(), tup[1].text()) for tup in self.e_name_pairs]
			hasher.dat_hasher(self.ovl_data, names)
			self.update_gui_table()
		else:
			util.interaction.showdialog("You must open an OVL file before you can extract files!")
			
	def remover(self):
		if self.file_widget.filename:
			remove_text = self.remove.text()
			remover.file_remover(self.ovl_data, remove_text)
			self.update_gui_table()
		else:
			util.interaction.showdialog("You must open an OVL file before you can remove files!")

	def walker_hash(self, dummy=False, walk_ovls=True, walk_models=True):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"), )
		hash_dict = {}
		if start_dir:
			# don't use internal data
			ovl_data = OvlFile()
			error_files = []
			ovl_files = walker.walk_type(start_dir, extension="ovl")
			of_max = len(ovl_files)
			for of_index, ovl_path in enumerate(ovl_files):
				self.update_progress("Hashing names: " + os.path.basename(ovl_path), value=of_index, vmax=of_max)
				try:
					# read ovl file
					new_hashes = ovl_data.load(ovl_path, commands=("generate_hash_table",))
					hash_dict.update(new_hashes)
				except:
					error_files.append(ovl_path)
			if error_files:
				print(f"{error_files} caused errors!")
			# write the hash text file to the hashes folder
			export_dir = os.path.join(os.getcwd(), "hashes")
			out_path = os.path.join(export_dir, f"{os.path.basename(start_dir)}.txt")
			with open(out_path, "w") as f:
				for k, v in hash_dict.items():
					f.write(f"{k} = {v}\n")
			print(f"Wrote {len(hash_dict)} items to {out_path}")

	def walker(self, dummy=False, walk_ovls=True, walk_models=True):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg.get("dir_ovls_in", "C://"), )
		errors = []
		if start_dir:
			export_dir = os.path.join(start_dir, "walker_export")
			# don't use internal data
			ovl_data = OvlFile()
			mdl2_data = Mdl2File()
			if walk_ovls:
				error_files = []
				skip_files = []
				ovl_files = walker.walk_type(start_dir, extension="ovl")
				of_max = len(ovl_files)
				for of_index, ovl_path in enumerate(ovl_files):
					self.update_progress("Walking OVL files: " + os.path.basename(ovl_path), value=of_index, vmax=of_max)
					try:
						# read ovl file
						ovl_data.load(ovl_path, commands=self.commands)
						# create an output folder for it
						outdir = os.path.join(export_dir, os.path.basename(ovl_path[:-4]))
						# create output dir
						os.makedirs(outdir, exist_ok=True)
						error_files_new, skip_files_new = extract.extract(ovl_data.ovs_files[0], outdir, only_types=["ms2", ])
						error_files += error_files_new
						skip_files += skip_files_new
					except Exception as ex:
						traceback.print_exc()
						errors.append((ovl_path, ex))

				self.skip_messages(error_files, skip_files)

			# holds different types of flag - list of byte maps pairs
			type_dic = {}
			if walk_models:
				mdl2_files = walker.walk_type(export_dir, extension="mdl2")
				mf_max = len(mdl2_files)
				for mf_index, mdl2_path in enumerate(mdl2_files):
					mdl2_name = os.path.basename(mdl2_path)
					self.update_progress("Walking MDL2 files: " + mdl2_name, value=mf_index, vmax=mf_max)
					try:
						mdl2_data.load(mdl2_path, quick=True, map_bytes=True)
						for model in mdl2_data.models:
							if model.flag not in type_dic:
								type_dic[model.flag] = ([], [])
							type_dic[model.flag][0].append(mdl2_name)
							type_dic[model.flag][1].append(model.bytes_map)
					except Exception as ex:
						traceback.print_exc()
						errors.append((mdl2_path, ex))
			# report
			print("\nThe following errors occured:")
			for file_path, ex in errors:
				print(file_path, str(ex))

			print("\nThe following type - map pairs were found:")
			for flag, tup in sorted(type_dic.items()):
				print(flag, bin(flag))
				names, maps_list = tup
				print("Some files:", list(set(names))[:25])
				print("num models", len(maps_list))
				print("mean", np.mean(maps_list, axis=0).astype(dtype=np.ubyte))
				print("max", np.max(maps_list, axis=0))
				print()

			self.update_progress("Operation completed!", value=1, vmax=1)

	def closeEvent(self, event):
		if self.file_widget.dirty:
			qm = QtWidgets.QMessageBox
			quit_msg = "You will lose unsaved work on "+os.path.basename(self.file_widget.filepath)+"!"
			reply = qm.question(self, 'Quit?', quit_msg, qm.Yes, qm.No)

			if reply == qm.Yes:
				event.accept()
			else:
				event.ignore()
		else:
			event.accept()

	@staticmethod
	def check_version():
		is_64bits = sys.maxsize > 2 ** 32
		if not is_64bits:
			util.interaction.showdialog("Either your operating system or your python installation is not 64 bits.\n"
							   "Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] < 7 or (sys.version_info[1] == 7 and sys.version_info[2] < 6):
			util.interaction.showdialog("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	print("running python", sys.version)
	widgets.startup(MainWindow)
