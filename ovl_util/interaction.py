import logging

from PyQt5 import QtWidgets


def showdialog(info, ask=False, details=None):
	msg = QtWidgets.QMessageBox()
	msg.setIcon(QtWidgets.QMessageBox.Information)
	msg.setText(info)
	if ask:
		msg.setWindowTitle("Question")
		msg.setStandardButtons(msg.Yes | msg.No)
	else:
		msg.setWindowTitle("Error")
		msg.setStandardButtons(msg.Ok)
		if details:
			msg.setDetailedText(details)
	return msg.exec_() == msg.Yes


def extract_error_warning(error_files):
	if error_files:
		logging.warning("Files not extracted due to error:")
		for ef in error_files:
			logging.warning(ef)

		message = f"{len(error_files)} files have errored and were not extracted."
		showdialog(message)
