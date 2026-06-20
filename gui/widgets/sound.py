import logging
import math

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QBuffer, QIODevice, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QSlider, QWidget, QLabel, QCheckBox, QGridLayout
from PyQt5.QtMultimedia import QAudio, QAudioFormat, QAudioOutput

from gui.app_utils import get_icon



import sys
from PyQt5.QtCore import QUrl, QTime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaContent


class AudioWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.player = QMediaPlayer()
		self.player.stateChanged.connect(self.audio_state_changed)
		self.player.positionChanged.connect(self.update_cursor)
		self.player.durationChanged.connect(self.changed_duration)
		self.player.setNotifyInterval(50)

		self.volume_label = QLabel()
		self.volume_label.setPixmap(get_icon("volume").pixmap(16))
		
		self.volume_slider = QSlider(Qt.Horizontal)
		self.volume_slider.setMinimum(0)
		self.volume_slider.setMaximum(100)
		self.volume_slider.setPageStep(1)
		self.volume_slider.setValue(50)
		self.volume_slider.valueChanged.connect(self.change_volume)
		self.change_volume(self.volume_slider.value())

		self.time_slider = QSlider(Qt.Horizontal)
		self.time_slider.setMinimum(0)
		self.time_slider.setMaximum(1000)
		self.time_slider.setPageStep(1)
		self.time_slider.setValue(0)
		self.time_slider.sliderMoved.connect(self.seek)
		self.time_label = QLabel()
		font = QtGui.QFont("Monospace")
		font.setStyleHint(QtGui.QFont.TypeWriter)
		self.time_label.setFont(font)
		self.update_cursor(0)

		self.play_button = QPushButton()
		self.play_button.setIcon(get_icon("play"))

		self.stop_button = QPushButton()
		self.stop_button.setIcon(get_icon("stop"))

		self.play_button.clicked.connect(self.play_pause)
		self.stop_button.clicked.connect(self.player.stop)

		layout = QGridLayout(self)
		layout.setContentsMargins(8, 0, 0, 0)
		layout.setHorizontalSpacing(3)
		layout.setVerticalSpacing(0)
		layout.addWidget(self.play_button, 0, 0)
		layout.addWidget(self.stop_button, 0, 1)
		layout.addWidget(self.volume_label, 0, 2)
		layout.addWidget(self.volume_slider, 0, 3)
		layout.addWidget(self.time_slider, 1, 0, 1, 4)
		layout.addWidget(self.time_label, 1, 5)

		# layout = QHBoxLayout(self)
		# layout.addWidget(self.play_button)
		# layout.addWidget(self.stop_button)
		# layout.addWidget(self.time_slider)
		# layout.addWidget(self.time_label)
		# layout.addWidget(self.volume_label)
		# layout.addWidget(self.volume_slider)
		# layout.addStretch()

	def play_pause(self):
		if self.player.state() == QMediaPlayer.PlayingState:
			self.player.pause()
		else:
			self.player.play()

	def audio_state_changed(self, new_state):
		# adjust the button icon
		if self.player.state() == QMediaPlayer.PlayingState:
			self.play_button.setIcon(get_icon("pause"))
		else:
			self.play_button.setIcon(get_icon("play"))

	def changed_duration(self, duration):
		self.update_cursor(0)

	def seek(self, slider_value):
		if self.player.duration():
			cursor = int(slider_value / 1000 * self.player.duration())
			self.player.setPosition(cursor)
			self.update_label(cursor)

	def update_cursor(self, cursor):
		if self.player.duration():
			self.time_slider.setValue(int(cursor / self.player.duration() * 1000))
		self.update_label(cursor)

	def update_label(self, cursor):
		self.time_label.setText(f"{sec_to_timestamp(cursor / 1000)} / {sec_to_timestamp(self.player.duration() / 1000)}")

	def change_volume(self, value):
		linearVolume = int(QAudio.convertVolume(value / self.volume_slider.maximum(), QAudio.LogarithmicVolumeScale,
										QAudio.LinearVolumeScale) * 100)
		self.player.setVolume(linearVolume)

	def load_file(self, file_path):
		media = QMediaContent(QUrl.fromLocalFile(file_path))
		self.player.setMedia(media)


def sec_to_timestamp(t):
	m, s = divmod(t, 60)
	s, ms = divmod(s * 1000, 1000)
	return f"{m:02.0f}:{s:02.0f}:{ms:03.0f}"
