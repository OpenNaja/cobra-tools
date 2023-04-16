import logging

from PyQt5 import QtWidgets

def showdialog(info, title="", buttons=None, details=None):
	msg = QtWidgets.QMessageBox()
	msg.setIcon(QtWidgets.QMessageBox.Information)
	msg.setText(info)
	msg.setWindowTitle(title)
	msg.setStandardButtons(msg.Ok if not buttons else buttons)
	if details:
		msg.setDetailedText(details)
	return msg.exec_() not in [msg.No, msg.Cancel]

def showquestion(info, title=None, details=None):
	return showdialog(info, title="Question" if not title else title, 
					  buttons=(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No), details=details)

def showconfirmation(info, title=None, details=None):
	return showdialog(info, title="Confirm" if not title else title,
					  buttons=(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel), details=details)

def showwarning(info, details=None):
	return showdialog(info, title="Warning", details=details)

def showerror(info, details=None):
	return showdialog(info, title="Error", details=details)


def extract_error_warning(error_files):
	if error_files:
		logging.warning("Files not extracted due to error:")
		for ef in error_files:
			logging.warning(ef)

		message = f"{len(error_files)} files have errored and were not extracted."
		showdialog(message)
