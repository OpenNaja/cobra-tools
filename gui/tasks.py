
import logging
from typing import Any, AnyStr, Union, Optional, Iterable, Callable, cast, NamedTuple, Literal

from modules.formats.shared import DummyReporter

from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg  # pyright: ignore  # noqa: F401
from PyQt5.QtCore import (pyqtSignal, pyqtSlot, Qt, QObject, QRunnable)

class WorkerSignals(QObject):
	'''
	Defines the signals available from a running worker thread.
	Supported signals are:
	- finished: No data
	- error:`tuple` (exctype, value, traceback.format_exc() )
	- result: `object` data returned from processing, anything
	- progress: `tuple` indicating progress metadata
	'''
	result = pyqtSignal(object)
	# progress = pyqtSignal(tuple)
	finished = pyqtSignal()
	error_msg = pyqtSignal(str)


class WorkerRunnable(QRunnable):

	def __init__(self, func: Callable, *args, **kwargs) -> None:
		super().__init__()
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()
		self._is_cancelled = False
		self.setAutoDelete(True)

	@pyqtSlot()
	def run(self) -> None:
		if self._is_cancelled:
			logging.info(f"Worker for {self.func.__name__} cancelled before execution.")
			self.signals.finished.emit()  # Still signal completion of the runnable
			return
		try:
			# Check if the target function can accept a cancellation check
			import inspect
			sig = inspect.signature(self.func)
			if 'cancellation_check' in sig.parameters:
				# If so, inject our cancellation check method
				self.kwargs['cancellation_check'] = lambda: self._is_cancelled
			result_data = self.func(*self.args, **self.kwargs)
			if not self._is_cancelled and result_data is not None:
				self.signals.result.emit(result_data)
		except Exception as err:
			# Check if cancellation happened and func perhaps raised an error because of it
			if self._is_cancelled:
				logging.info(f"Worker for {self.func.__name__} errored, possibly due to cancellation: {err}")
			else:
				logging.exception(f"Threaded call of function '{self.func.__name__}()' errored!")
				#if not self._is_cancelled:
				self.signals.error_msg.emit(str(err))
		finally:
			self.signals.finished.emit()

	def cancel(self) -> None:
		logging.info(f"Cancel requested for worker: {getattr(self.func, '__name__', 'unknown_func')}")
		self._is_cancelled = True


class Reporter(DummyReporter, QObject):
	"""A class wrapping the interaction between OvlFile and the UI"""
	warning_msg = pyqtSignal(tuple)  # type: ignore
	success_msg = pyqtSignal(str)  # type: ignore
	files_list = pyqtSignal(list)  # type: ignore
	included_ovls_list = pyqtSignal(list)  # type: ignore
	progress_percentage = pyqtSignal(int)  # type: ignore
	progress_total = pyqtSignal(int)  # type: ignore
	current_action = pyqtSignal(str)  # type: ignore