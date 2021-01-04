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