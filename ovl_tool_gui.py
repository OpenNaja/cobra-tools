import os
import sys
import traceback
import time
from PyQt5 import QtWidgets
import numpy as np

from pyffi_ext.formats.ovl import OvlFormat
from pyffi_ext.formats.ms2 import Ms2Format
from util import widgets
from modules import extract, inject, hasher, walker

from generated.formats.ovl import OvlFile


class MainWindow(widgets.MainWindow):

	def __init__(self):
		widgets.MainWindow.__init__(self, "OVL Tool", )

		self.ovl_data = OvlFile()

		supported_types = ("DDS", "PNG", "MDL2", "TXT", "FGM", "FDB", "MATCOL", "XMLCONFIG", "ASSETPKG", "LUA", "WEM","OTF","TTF")
		self.filter = "Supported files ({})".format( " ".join("*."+t for t in supported_types) )

		self.file_widget = widgets.FileWidget(self, self.cfg)
		self.file_widget.setToolTip("The name of the OVL file that is currently open.")

		#self.e_name_pairs = [ (QtWidgets.QLineEdit("old"), QtWidgets.QLineEdit("new")) for i in range(3) ]

		self.p_action = QtWidgets.QProgressBar(self)
		self.p_action.setGeometry(0, 0, 200, 15)
		self.p_action.setTextVisible(True)
		self.p_action.setMaximum(1)
		self.p_action.setValue(0)
		self.t_action_current_message = "No operation in progress"
		self.t_action = QtWidgets.QLabel(self, text = self.t_action_current_message)
		
		# toggles
		self.t_write_dds = QtWidgets.QCheckBox("Save Temp Files")
		self.t_write_dds.setToolTip("By default, temporary files are converted to usable ones and back on the fly.")
		self.t_write_dds.setChecked(False)
		
		self.t_2K = QtWidgets.QCheckBox("Inject 2K")
		self.t_2K.setToolTip("Experimental: Increase a JWE Diffuse or Normal map to 2048x2048 resolution.")
		self.t_2K.setChecked(False)
		
		self.t_write_dat = QtWidgets.QCheckBox("Save DAT")
		self.t_write_dat.setToolTip("Writes decompressed archive streams to DAT files for debugging.")
		self.t_write_dat.setChecked(False)
		self.t_write_dat.stateChanged.connect(self.load_ovl)

		self.t_write_frag_log = QtWidgets.QCheckBox("Save Frag Log")
		self.t_write_frag_log.setToolTip("For devs.")
		self.t_write_frag_log.setChecked(False)
		self.t_write_frag_log.stateChanged.connect(self.load_ovl)
        
		self.spacer = QtWidgets.QLabel(self, text = "       ")
		self.ext_desc = QtWidgets.QLabel(self, text = "Check which filetypes to extract")
		self.ext_fdb = QtWidgets.QCheckBox("Extract FDB Files")
		self.ext_fdb.setChecked(True)
		self.ext_lua = QtWidgets.QCheckBox("Extract LUA Files")
		self.ext_lua.setChecked(False)
		self.ext_anim = QtWidgets.QCheckBox("Extract Animation Files")
		self.ext_anim.setChecked(True)
		self.ext_model = QtWidgets.QCheckBox("Extract Model Files")
		self.ext_model.setChecked(True)
		self.ext_tex = QtWidgets.QCheckBox("Extract Texture Files")
		self.ext_tex.setChecked(True)
		self.ext_txt = QtWidgets.QCheckBox("Extract Text Files")
		self.ext_txt.setChecked(False)
		self.ext_shader = QtWidgets.QCheckBox("Extract Material Files")
		self.ext_shader.setChecked(True)
		self.ext_aux = QtWidgets.QCheckBox("Extract Audio Files")
		self.ext_aux.setChecked(True)
		self.ext_fct = QtWidgets.QCheckBox("Extract Font Files")
		self.ext_fct.setChecked(True)
		self.ext_misc = QtWidgets.QCheckBox("Extract Misc Files")
		self.ext_misc.setChecked(False)


		self.qgrid = QtWidgets.QGridLayout()
		self.qgrid.addWidget(self.file_widget, 0, 0, 1, 2)		
		self.qgrid.addWidget(self.p_action, 1, 0, 1, 2)
		self.qgrid.addWidget(self.t_action, 2, 0, 1, 2)		
		self.qgrid.addWidget(self.t_write_dds, 3, 0)
		self.qgrid.addWidget(self.t_write_dat, 4, 0)
		self.qgrid.addWidget(self.t_write_frag_log, 5, 0)
		self.qgrid.addWidget(self.t_2K, 6, 0)

		self.qgrid.addWidget(self.spacer, 0, 2)
		self.qgrid.addWidget(self.ext_desc, 0, 3)
		self.qgrid.addWidget(self.ext_fdb, 1, 3)
		self.qgrid.addWidget(self.ext_lua, 2, 3)
		self.qgrid.addWidget(self.ext_anim, 3, 3)
		self.qgrid.addWidget(self.ext_model, 4, 3)
		self.qgrid.addWidget(self.ext_tex, 5, 3)
		self.qgrid.addWidget(self.ext_shader, 6, 3)
		self.qgrid.addWidget(self.ext_txt, 7, 3)
		self.qgrid.addWidget(self.ext_aux, 8, 3)
		self.qgrid.addWidget(self.ext_fct, 9, 3)
		self.qgrid.addWidget(self.ext_misc, 10, 3)
		#start = 7
		#for i, (old, new) in enumerate(self.e_name_pairs):
		#	self.qgrid.addWidget(old, start+i, 0)
		#	self.qgrid.addWidget(new, start+i, 1)
        
		self.central_widget.setLayout(self.qgrid)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('File')
		editMenu = mainMenu.addMenu('Edit')
		helpMenu = mainMenu.addMenu('Help')
		button_data = ((fileMenu, "Open", self.file_widget.ask_open, "CTRL+O", "SP_DirIcon"),
					   (fileMenu, "Save", self.save_ovl, "CTRL+S", "SP_DriveFDIcon"),
					   (fileMenu, "Exit", self.close, "", "SP_DialogCloseButton"),
					   (editMenu, "Unpack", self.extract_all, "CTRL+U", ""),
					   (editMenu, "Inject", self.inject, "CTRL+I", ""),
					   (editMenu, "Hash", self.hasher, "CTRL+H", ""),
					   (editMenu, "Walk", self.walker, "", ""),
					   (helpMenu, "Report Bug", self.report_bug, "", "SP_MessageBoxCritical"),
					   (helpMenu, "Documentation", self.online_support, "", "SP_MessageBoxInformation"))
		self.add_to_menu(button_data)
		self.check_version()

	@property
	def commands(self,):
		# get those commands that are set to True
		return [ x for x in ("write_dat", "write_frag_log") if getattr(self, x)]

	@property
	def ovl_name(self,):
		return self.file_widget.entry.text()

	@ovl_name.setter
	def ovl_name(self, name):
		self.file_widget.setText(name)

	@property
	def write_dds(self,):
		return self.t_write_dds.isChecked()
	
	@property
	def write_2K(self,):
		return self.t_2K.isChecked()
        
	@property
	def extract_fdb(self,):
		return self.ext_fdb.isChecked()
        
	@property
	def extract_lua(self,):
		return self.ext_lua.isChecked()
        
	@property
	def extract_anim(self,):
		return self.ext_anim.isChecked()
        
	@property
	def extract_model(self,):
		return self.ext_model.isChecked()

	@property
	def extract_tex(self,):
		return self.ext_tex.isChecked()

	@property
	def extract_shader(self,):
		return self.ext_shader.isChecked()

	@property
	def extract_text(self,):
		return self.ext_txt.isChecked()
        
	@property
	def extract_aux(self,):
		return self.ext_aux.isChecked()
        
	@property
	def extract_fct(self,):
		return self.ext_fct.isChecked()
        
	@property
	def extract_misc(self,):
		return self.ext_misc.isChecked()
	
	@property
	def write_dat(self,):
		return self.t_write_dat.isChecked()

	@property
	def write_frag_log(self,):
		return self.t_write_frag_log.isChecked()

	def update_commands(self):
		# at some point, just set commands to archive and trigger changes there
		if self.ovl_name:
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
		
	def load_ovl(self):
		if self.file_widget.filepath:
			self.file_widget.dirty = False
			self.cfg["dir_ovls_in"], ovl_name = os.path.split(self.file_widget.filepath)
			start_time = time.time()			
			self.update_progress("Reading OVL " + self.file_widget.filepath, value=0, vmax=0)
			try:
				self.ovl_data.load(self.file_widget.filepath, commands=self.commands)
				self.ovl_name = ovl_name
			except Exception as ex:
				traceback.print_exc()
				widgets.showdialog(str(ex))
				print(ex)
			print(f"Done in {time.time()-start_time:.2f} seconds!")
			self.update_progress("Operation completed!", value=1, vmax=1)
		
	def save_ovl(self):
		if self.ovl_name:
			file_src = QtWidgets.QFileDialog.getSaveFileName(self, 'Save OVL', os.path.join(self.cfg["dir_ovls_out"], self.ovl_name), "OVL files (*.ovl)",)[0]
			if file_src:
				self.cfg["dir_ovls_out"], ovl_name = os.path.split(file_src)
				# just a dummy stream
				try:
					self.ovl_data.save(file_src)
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
			widgets.showdialog(message)
	
	def extract_all(self):
		if self.ovl_name:
			self.cfg["dir_extract"] = QtWidgets.QFileDialog.getExistingDirectory(self, 'Output folder', self.cfg["dir_extract"], )
			if self.cfg["dir_extract"]:
				dir = self.cfg["dir_extract"]
				# create output dir
				try:
					os.makedirs(dir, exist_ok=True)
					archive = self.ovl_data.ovs_files[0]
					archive.dir = dir
					error_files, skip_files = extract.extract(archive, self.extract_fdb, self.extract_lua, self.extract_anim, self.extract_model, self.extract_tex, self.extract_shader, self.extract_text, self.extract_aux, self.extract_fct, self.extract_misc, self.write_dds, progress_callback=self.update_progress)

					self.skip_messages(error_files, skip_files)
					self.update_progress("Operation completed!", value=1, vmax=1)
				except Exception as ex:
					traceback.print_exc()
					widgets.showdialog(str(ex))
					print(ex)
		else:
			widgets.showdialog("You must open an OVL file before you can extract files!")
			
	def inject(self):
		if self.ovl_name:
			files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Inject files', self.cfg["dir_inject"], self.filter)[0]
			if files:
				self.cfg["dir_inject"] = os.path.dirname(files[0])
			try:
				inject.inject(self.ovl_data, files, self.write_dds, self.write_2K)
				self.file_widget.dirty = True
			except Exception as ex:
				traceback.print_exc()
				widgets.showdialog(str(ex))
			print("Done!")
		else:
			widgets.showdialog("You must open an OVL file before you can inject files!")

	def hasher(self):
		if self.ovl_name:
			names = [ (tup[0].text(), tup[1].text()) for tup in self.e_name_pairs ]
			for archive in self.ovl_data.archives:
				hasher.dat_hasher(archive, names, self.ovl_data.header.files, self.ovl_data.header.textures)
		else:
			widgets.showdialog("You must open an OVL file before you can extract files!")

	def walker(self, dummy=False, walk_ovls=True, walk_models=True):
		start_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Game Root folder', self.cfg["dir_ovls_in"], )
		errors = []
		if start_dir:
			export_dir = os.path.join(start_dir, "walker_export")
			# don't use internal data
			ovl_data = OvlFormat.Data()
			mdl2_data = Ms2Format.Data()
			if walk_ovls:
				error_files = []
				skip_files = []
				ovl_files = walker.walk_type(start_dir, extension="ovl")
				of_max = len(ovl_files)
				for of_index, ovl_path in enumerate(ovl_files):
					self.update_progress("Walking OVL files: " + os.path.basename(ovl_path), value=of_index, vmax=of_max)
					try:
						# read ovl file
						with open(ovl_path, "rb") as ovl_stream:
							ovl_data.read(ovl_stream, file=ovl_path, commands=self.commands, mute=True)
						# create an output folder for it
						outdir = os.path.join(export_dir, os.path.basename(ovl_path[:-4]))
						# create output dir
						os.makedirs(outdir, exist_ok=True)
						for archive in ovl_data.archives:
							archive.dir = outdir
							error_files_new, skip_files_new = extract.extract(archive, self.write_dds, only_types=["ms2", ])#, progress_callback=self.update_progress)
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
						with open(mdl2_path, "rb") as mdl2_stream:
							mdl2_data.read(mdl2_stream, file=mdl2_path, quick=True, map_bytes=True)
							for model in mdl2_data.mdl2_header.models:
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
			for flag, tup in type_dic.items():
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
			widgets.showdialog("Either your operating system or your python installation is not 64 bits.\n"
							   "Large OVLs will crash unexpectedly!")
		if sys.version_info[0] != 3 or sys.version_info[1] < 7 or (sys.version_info[1] == 7 and sys.version_info[2] < 6):
			widgets.showdialog("Python 3.7.6+ x64 bit is expected!")


if __name__ == '__main__':
	print("running python", sys.version)
	widgets.startup(MainWindow)
