from PyQt5 import QtCore
import time
import functools
import logging
# from util import resampling, io_ops, fourier


# nb. in QThreads, run() is called when start() is called on class
from generated.formats.ovl import OvlFile


class OvlThread(QtCore.QThread):
	# notifyProgress = QtCore.pyqtSignal(int)

	def __init__(self, progress_callback=None):
		super().__init__()
		# if progress_callback:
		# 	self.notifyProgress.connect(progress_callback)

		self.ovl_data = OvlFile(progress_callback=progress_callback)
		self.func = None
		self.args = ()
		self.kwargs = {}

	def run(self):
		self.func(*self.args, **self.kwargs)


class Runner(QtCore.QThread):

	def __init__(self, target, *args, **kwargs):
		super().__init__()
		self._target = target
		self._args = args
		self._kwargs = kwargs

	def run(self):
		self._target(*self._args, **self._kwargs)


def run(func):
	@functools.wraps(func)
	def async_func(*args, **kwargs):
		runner = Runner(func, *args, **kwargs)
		# Keep the runner somewhere or it will be destroyed
		func.__runner = runner
		runner.start()

	return async_func


@run
def test(a):
	time.sleep(3)
	print('TEST', a)


class Runnable(QtCore.QRunnable):

	def __init__(self, n, args, kwargs):
		super().__init__()
		self.n = n
		self.args = args
		self.kwargs = kwargs

	def run(self):
		self.n(*self.args, **self.kwargs)


def runTask(n, args, kwargs):
	# threadCount = QtCore.QThreadPool.globalInstance().maxThreadCount()
	# logging.info(f"Running {threadCount} Threads")
	pool = QtCore.QThreadPool.globalInstance()
	# for i in range(threadCount):
	# 	# 2. Instantiate the subclass of QRunnable
	runnable = Runnable(n, args, kwargs)
	# 3. Call start()
	pool.start(runnable)
