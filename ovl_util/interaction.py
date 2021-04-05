from PyQt5 import QtWidgets


def showdialog(info, ask=False):
	msg = QtWidgets.QMessageBox()
	msg.setIcon(QtWidgets.QMessageBox.Information)
	msg.setText(info)
	if ask:
		msg.setWindowTitle("Question")
		msg.setStandardButtons(msg.Yes | msg.No)
	else:
		msg.setWindowTitle("Error")
		msg.setStandardButtons(msg.Ok)
	return msg.exec_() == msg.Yes


def skip_messages(error_files, skip_files):
	error_count = len(error_files)
	skip_count = len(skip_files)
	if error_count:
		print("Files not extracted due to error:")
		for ef in error_files:
			print("\t", ef)

	if skip_count:
		print("Unsupported files not extracted:")
		for sf in skip_files:
			print("\t", sf)

	if error_count or skip_count:
		message = f"{error_count + skip_count} files were not extracted from the archive and may be missing from the output folder. {skip_count} were unsupported, while {error_count} produced errors."
		showdialog(message)
