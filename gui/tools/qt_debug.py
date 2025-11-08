import os
import re
import inspect
import logging
import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable, Any, Iterable, Generator
if TYPE_CHECKING:
	from PyQt5.QtCore import QTimer, QObject
	from pytest import MonkeyPatch, FixtureRequest


class DebugState:
	"""Manages the global state for the debugging tools"""
	qtimer_debug_active: bool = False
	signal_debug_active: bool = False
	# Flag to control the singleShot behavior. When True, singleShot calls are immediate.
	qtimer_singleshot_immediate: bool = False
	qtimer_immediate_threshold: int = -1
	originals: dict = {
		"QTimer.__init__": None,
		"QTimer.start": None,
		"QTimer.stop": None,
		"QTimer.singleShot": None,
		"pyqtBoundSignal.connect": None,
	}
	signal_ignore_patterns: set[str] = set()
	compiled_ignore_regex: re.Pattern | None = None
	qtimer_ignore_patterns: set[str] = set()
	ignored_qtimer_ids: set[int] = set()


class SimpleMonkeyPatch:
	"""Mimic pytest's monkeypatch.setattr for live use"""
	def setattr(self, target, name, new_value):
		setattr(target, name, new_value)


from types import SimpleNamespace
# Mimics the pytest 'request.node.name' structure
app_request_placeholder = SimpleNamespace(
	node=SimpleNamespace(name="LiveApp")
)


# Use thread-local storage for a re-entrancy guard
_tracer_guard = threading.local()

@contextmanager
def guarded_tracer() -> Generator[bool, Any, None]:
	"""
	A context manager to prevent re-entrant calls to the tracers.
	Yields True if it's safe to trace, False otherwise.
	"""
	if getattr(_tracer_guard, 'is_tracing', False):
		yield False
		return

	try:
		_tracer_guard.is_tracing = True
		yield True
	finally:
		_tracer_guard.is_tracing = False


_early_log_config_done = False
def _configure_early_logging():
	"""
	Ensures a basic console logger is active at the DEBUG level.
	"""
	global _early_log_config_done
	if _early_log_config_done:
		return

	root_logger = logging.getLogger()
	
	# If the root logger has no handlers, logging is unconfigured
	if not root_logger.hasHandlers():
		import sys
		handler = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter('[EARLY DEBUG] %(message)s')
		handler.setFormatter(formatter)
		root_logger.addHandler(handler)

	root_logger.setLevel(logging.DEBUG)
	_early_log_config_done = True


def _get_caller_qualname(stack_depth: int = 2) -> str:
	"""
	Walks the stack to find the fully qualified name of the caller,
	e.g., 'ClassName.method_name'.
	"""
	try:
		stack = inspect.stack()
		for frame_info in stack[stack_depth:]:
			if __file__ not in frame_info.filename:
				return frame_info.frame.f_code.co_qualname
		return "unknown"
	except Exception:
		return "unknown"


def _get_caller_info(stack_depth: int = 2) -> str:
	"""
	Walks the stack to find the file, line number, and function name of the caller.
	Returns a tuple containing the formatted string (path:line (func)) and
	the full FrameInfo object for further inspection.
	"""
	from gui import root_dir
	try:
		stack = inspect.stack()
		# Find the first frame that is outside of this current file.
		for frame_info in stack[stack_depth:]:
			if __file__ not in frame_info.filename:
				caller_abs_path = frame_info.filename
				try:
					# Calculate path relative to the project root
					caller_rel_path = os.path.relpath(caller_abs_path, root_dir)
				except ValueError:
					# Fallback for files outside the project
					caller_rel_path = os.path.basename(caller_abs_path)
				
				# Normalize
				caller_rel_path = caller_rel_path.replace(os.sep, '/')
				return (
					f"{caller_rel_path}:{frame_info.lineno} "
					f"({frame_info.function})"
				), frame_info
		return "unknown location"
	except Exception:
		return "unknown location (error during stack inspection)"


# -------------------------------------------------------------------------- #
#                             QTimer Debugger                                #
# region ------------------------------------------------------------------- #

@contextmanager
def immediate_singleshot_timers(threshold: int = -1) -> Generator[None, Any, None]:
	"""
	A context manager to temporarily force QTimer.singleShot calls
	to execute their callback immediately instead of posting to the event loop.

	Useful for debugging re-entrancy issues during tests.

	Example:
		from tests.test_gui.qt_debug import immediate_singleshot_timers
		with immediate_singleshot_timers():
			do_something_that_uses_singleshot()
	Args:
		threshold: The interval threshold in milliseconds. singleShot calls
		           with a duration less than or equal to this value will be
		           made immediate. A value of -1 (default) makes all
		           singleShot timers immediate.
	"""
	original_state = DebugState.qtimer_singleshot_immediate
	original_threshold = DebugState.qtimer_immediate_threshold
	DebugState.qtimer_singleshot_immediate = True
	DebugState.qtimer_immediate_threshold = threshold
	log_msg = f"IMMEDIATE singleShot (threshold <= {threshold}ms)." if threshold >= 0 else "IMMEDIATE singleShot (all)."
	logging.debug(f"[QTIMER.MODE] ==> Switched to {log_msg}")
	try:
		yield
	finally:
		DebugState.qtimer_singleshot_immediate = original_state
		DebugState.qtimer_immediate_threshold = original_threshold
		logging.debug("[QTIMER.MODE] <== Restored normal (queued) singleShot execution.")


def install_qtimer_tracer(ignore: Iterable[str] | None = None):
	"""
	Sets up and applies the QTimer tracing patches.

	Args:
		ignore: An optional iterable of patterns to ignore. Supports formats:
				1. Assigned Variable Name (e.g. "fetchTimer") to ignore a
				   specific timer instance for its entire lifetime.
				2. Qualified Function Name (e.g. "LogView.startFetches")
				   to ignore any timer started by that specific function.
				3. [singleShot()] Function Name (e.g. "perform_initial_layout") or
				   Qual Name (e.g. "MainWindow.perform_initial_layout") to ignore
				   QTimer.singleShot(callback).
	"""
	_configure_early_logging()
	if DebugState.qtimer_debug_active:
		logging.debug("QTimer tracing is already installed.")
		return

	if ignore:
		DebugState.qtimer_ignore_patterns.update(ignore)

	# Pass pytest-compatible objects
	_trace_qtimer_calls(SimpleMonkeyPatch(), app_request_placeholder)
	
	# Add QTimer.timeout to the signal ignore list
	DebugState.signal_ignore_patterns.add("QTimer.timeout")
	DebugState.qtimer_debug_active = True
	logging.debug("QTimer tracing has been installed.")

	# If signal tracer is already active, we need to update its regex
	if DebugState.signal_debug_active:
		_recompile_signal_ignore_regex()


def _trace_qtimer_calls(
	monkeypatch: 'MonkeyPatch | SimpleMonkeyPatch',
	request: 'FixtureRequest | SimpleNamespace'
) -> None:
	"""
	Wraps QTimer methods to log their activity, including the file, line number,
	and function where they were called. This helps trace non-sequential,
	timer-driven events that might be causing state leakage.

	Written in a pytest compatible manner for use in fixtures.
	"""
	from PyQt5.QtCore import QTimer

	# Store original methods once to prevent wrapping a wrapper
	if DebugState.originals["QTimer.singleShot"] is None:
		DebugState.originals["QTimer.singleShot"] = QTimer.singleShot
		DebugState.originals["QTimer.__init__"] = QTimer.__init__
		DebugState.originals["QTimer.start"] = QTimer.start
		DebugState.originals["QTimer.stop"] = QTimer.stop

	original_singleShot = DebugState.originals["QTimer.singleShot"]
	original_init = DebugState.originals["QTimer.__init__"]
	original_start = DebugState.originals["QTimer.start"]
	original_stop = DebugState.originals["QTimer.stop"]

	# Active Timer Tracking
	_active_timers: set[int] = set()
	# Test case context (if pytest)
	context = "" if request.node.name == "LiveApp" else f" (Context: {request.node.name})"

	# Patch the static QTimer.singleShot method
	def patched_singleShot(msec, *args):
		slot = args[-1]
		func_name = getattr(slot, '__name__', 'unknown_lambda')

		# Check callback name against ignore patterns
		# This handles both simple names and "ClassName.method" qualified names.
		func_qualname = getattr(slot, '__qualname__', func_name)
		if func_name in DebugState.qtimer_ignore_patterns or func_qualname in DebugState.qtimer_ignore_patterns:
			logging.debug(f"[QTIMER IGNORED] singleShot for callback '{func_qualname}'")
			return original_singleShot(msec, *args)

		call_location, _ = _get_caller_info()
		# Note: We can't easily track the lifetime of a static singleShot,
		# so we just report the active count of instance timers at this moment
		active_count = len(_active_timers)

		# Check the global flag to decide the execution path.
		if DebugState.qtimer_singleshot_immediate:
			threshold = DebugState.qtimer_immediate_threshold
			if threshold == -1 or msec <= threshold:
				logging.debug(
					f"[QTIMER.SINGLESHOT.IMMEDIATE] -({active_count:02})- Executing '{func_name}' now\n"
					f"                                   Called from: {call_location}{context}"
				)
				try:
					# The callable is the last argument. Execute it immediately
					slot()
				except Exception:
					# Log any exception from the immediate call to aid debugging
					logging.exception(
						f"Exception occurred during IMMEDIATE singleShot call to '{func_name}'"
					)
				# IMPORTANT: Do not call the original function, effectively bypassing the event loop
				return

		logging.debug(
			f"[QTIMER.SINGLESHOT] -({active_count:02})- Queued '{func_name}' in {msec}ms\n"
			f"                                   Called from: {call_location}{context}"
		)
		return original_singleShot(msec, *args)

	monkeypatch.setattr(QTimer, "singleShot", patched_singleShot)

	# Patch the QTimer instance methods
	def patched_init(self, *args, **kwargs):
		original_init(self, *args, **kwargs)
		with guarded_tracer() as should_trace:
			if not should_trace:
				return
			self._timer_id = id(self)
			self._timer_origin, frame_info = _get_caller_info()
			
			# Use the returned frame_info to get the code context
			if frame_info and frame_info.code_context:
				line = frame_info.code_context[0].strip()
				if '=' in line:
					assigned_name = line.split('=', 1)[0].strip()
					self._assigned_name = assigned_name.split('.')[-1]
				else:
					self._assigned_name = "unassigned"
			else:
				self._assigned_name = "unknown"

			# Check ignore rules based on the variable name
			if self._assigned_name in DebugState.qtimer_ignore_patterns:
				# If the name matches, add its ID to the ignore set for all future events.
				DebugState.ignored_qtimer_ids.add(self._timer_id)
				logging.debug(
					f"[QTIMER IGNORED] ID: {self._timer_id} at creation due to name '{self._assigned_name}'"
				)
				self.timeout.connect(lambda: _active_timers.discard(self._timer_id))
				return
			
			active_count = len(_active_timers)
			logging.debug(
				f"[QTIMER CREATED] -({active_count:02})- ID: {self._timer_id}{context}\n"
				f"                                Origin: {self._timer_origin}"
			)
			
			def log_timeout():
				if self._timer_id in DebugState.ignored_qtimer_ids:
					if self.isSingleShot():
						_active_timers.discard(self._timer_id)
					return
				# Log the count at the moment of timeout
				active_count = len(_active_timers)
				logging.debug(
					f"[QTIMER TIMEOUT] -({active_count:02})- ID: {self._timer_id}{context}\n"
					f"                                Origin: {self._timer_origin}"
				)
				# If it's a single-shot timer, it is now inactive
				if self.isSingleShot():
					_active_timers.discard(self._timer_id)
	
			# Connect our custom logger to the timeout signal
			self.timeout.connect(log_timeout)

	def patched_start(self, *args, **kwargs):
		with guarded_tracer() as should_trace:
			if should_trace:
				# Check if this timer instance is already on the ignore list
				if self._timer_id in DebugState.ignored_qtimer_ids:
					return original_start(self, *args, **kwargs)

				# Check if the caller's location matches a new ignore rule
				caller_qualname = _get_caller_qualname()
				if caller_qualname in DebugState.qtimer_ignore_patterns:
					DebugState.ignored_qtimer_ids.add(self._timer_id)
					logging.debug(
						f"[QTIMER IGNORED] ID: {self._timer_id} due to rule '{caller_qualname}'"
					)
					return original_start(self, *args, **kwargs)

				is_zero_ms_start = True  # args and args[0] == 0
				if DebugState.qtimer_singleshot_immediate and self.isSingleShot() and is_zero_ms_start:
					start_location, _ = _get_caller_info()
					logging.debug(
						f"[QTIMER.START.IMMEDIATE] - ID: {self._timer_id}{context} | Emitting timeout signal now\n"
						f"                                         Origin: {self._timer_origin}\n"
						f"                                         Started at: {start_location}"
					)
					try:
						# Manually trigger the connected slot instead of starting the timer
						self.timeout.emit()
					except Exception:
						logging.exception(f"Exception during IMMEDIATE timeout.emit() for timer ID {self._timer_id}")
					# Bypass the original_start call entirely
					return

				# Proceed with normal logging and activation
				_active_timers.add(self._timer_id)
				active_count = len(_active_timers)
				interval = args[0] if args else '(default)'
				start_location, _ = _get_caller_info()
				logging.debug(
					f"[QTIMER START] -({active_count:02})- ID: {self._timer_id}{context} | Interval: {interval}ms\n"
					f"                              Origin: {self._timer_origin}\n"
					f"                              Started at: {start_location}"
				)
		return original_start(self, *args, **kwargs)

	def patched_stop(self):
		with guarded_tracer() as should_trace:
			if should_trace:
				if self._timer_id in DebugState.ignored_qtimer_ids:
					_active_timers.discard(self._timer_id)
					return original_stop(self)

				# Log the count before marking it as inactive
				active_count = len(_active_timers)
				stop_location, _ = _get_caller_info()
				logging.debug(
					f"[QTIMER STOP] -({active_count:02})- ID: {self._timer_id}{context}\n"
					f"                             Origin: {self._timer_origin}\n"
					f"                             Stopped at: {stop_location}"
				)
				# The timer is now inactive
				_active_timers.discard(self._timer_id)
		return original_stop(self)

	monkeypatch.setattr(QTimer, "__init__", patched_init)
	monkeypatch.setattr(QTimer, "start", patched_start)
	monkeypatch.setattr(QTimer, "stop", patched_stop)

# endregion



# -------------------------------------------------------------------------- #
#                             Signal Debugger                                #
# region ------------------------------------------------------------------- #

def _recompile_signal_ignore_regex():
	"""
	Compiles a single regex pattern from the set of ignored signals in the
	global state and stores it.
	"""
	patterns = []
	if not DebugState.signal_ignore_patterns:
		DebugState.compiled_ignore_regex = None
		return

	for item in DebugState.signal_ignore_patterns:
		# Split "ClassName.signalName" into parts
		parts = item.split('.', 1)
		if len(parts) == 2:
			# Create a regex that matches: ^ClassName\.\d*signalName
			# This handles cases like "QTimer.2timeout" from an input of "QTimer.timeout"
			# and will match the start of a string like "QTimer.2timeout()"
			class_name, signal_name = parts
			pattern = rf"^{re.escape(class_name)}\.\d*{re.escape(signal_name)}"
			patterns.append(pattern)
	
	if patterns:
		DebugState.compiled_ignore_regex = re.compile("|".join(patterns))
		logging.debug(
			f"Recompiled signal ignore regex with {len(patterns)} patterns."
		)
	else:
		DebugState.compiled_ignore_regex = None


def install_signal_tracer(
	ignore: Iterable[str] | None = None
):
	"""
	Sets up and applies pyqtSignal tracing patches. Can be called multiple
	times to add new signals to the ignore list.

	Args:
		ignore: An optional iterable of signal names to ignore during tracing.
				Each string should be in the format "ClassName.signalName",
					 e.g., ["QTimer.timeout", "LogModel.number_fetched"].
	"""
	_configure_early_logging()
	if DebugState.signal_debug_active and not ignore:
		logging.debug(
			"Signal tracing is already installed with no new ignore patterns."
		)
		return
	
	if ignore:
		DebugState.signal_ignore_patterns.update(ignore)

	if DebugState.qtimer_debug_active:
		DebugState.signal_ignore_patterns.add("QTimer.timeout")

	_recompile_signal_ignore_regex()
	
	if not DebugState.signal_debug_active:
		_trace_pyqt_signals(SimpleMonkeyPatch(), app_request_placeholder)
	
	DebugState.signal_debug_active = True
	logging.debug("pyqtSignal tracing has been installed.")


def _trace_pyqt_signals(
	monkeypatch: 'MonkeyPatch | SimpleMonkeyPatch',
	request: 'FixtureRequest | SimpleNamespace'
) -> None:
	"""
	Wraps pyqtBoundSignal.connect to intercept all signal connections,
	creating a spy that logs when a signal is emitted and what arguments it carries.
	"""
	try:
		from PyQt5.QtCore import pyqtBoundSignal
		from PyQt5.QtWidgets import QApplication
	except ImportError:
		logging.error("Could not import PyQt5 components. Is PyQt5 installed?")
		return

	if DebugState.originals["pyqtBoundSignal.connect"] is None:
		DebugState.originals["pyqtBoundSignal.connect"] = pyqtBoundSignal.connect
	
	original_connect = DebugState.originals["pyqtBoundSignal.connect"]
	context = "" if request.node.name == "LiveApp" else f" (Context: {request.node.name})"

	def patched_connect(self: pyqtBoundSignal, slot: Callable, *args: Any, **kwargs: Any):
		"""A patched version of .connect() that wraps the real slot in a spy."""
		with guarded_tracer() as should_trace:
			if should_trace:
				try:
					signal_name = self.signal
					slot_name = getattr(slot, '__name__', 'unknown_lambda_or_callable')
					connect_location, _ = _get_caller_info()
					is_signal_slot = isinstance(slot, pyqtBoundSignal)
					connection_type = "Chained Signal" if is_signal_slot else "Callable Slot"

					logging.debug(
						f"[SIGNAL CONNECT] '{signal_name}' -> '{slot_name}' (Type: {connection_type})\n"
						f"                          Connected at: {connect_location}{context}"
					)
				except Exception as e:
					logging.error(f"Error during signal connection tracing: {e}")
					return original_connect(self, slot, *args, **kwargs)

		is_signal_slot = isinstance(slot, pyqtBoundSignal)  # Recalculate outside guard

		def spy_wrapper(*spy_args: Any, **spy_kwargs: Any):
			"""This function is called when the signal is emitted, before the original slot."""
			with guarded_tracer() as should_trace:
				if should_trace:
					try:
						sender_obj: 'QObject | None' = QApplication.instance().sender()
						ignore_pattern = DebugState.compiled_ignore_regex
						should_log = True
						# Check if the signal is in the ignore list before logging
						if ignore_pattern and sender_obj:
							sender_class = sender_obj.__class__.__name__
							# e.g., "QTimer.2timeout()"
							full_signal_id = f"{sender_class}.{self.signal}"
							if ignore_pattern.search(full_signal_id):
								should_log = False

						if should_log:
							sender_class_log = sender_obj.__class__.__name__ if sender_obj else "UnknownSender"
							formatted_args = ", ".join(repr(a) for a in spy_args)
							formatted_kwargs = ", ".join(f"{k}={v!r}" for k, v in spy_kwargs.items())
							all_args = f"({formatted_args}{', ' if formatted_args and formatted_kwargs else ''}{formatted_kwargs})"

							logging.debug(
								f"[SIGNAL EMIT] '{sender_class_log}.{self.signal}' -> '{slot_name}'\n"
								f"                       Args: {all_args}{context}"
							)
					except Exception as e:
						logging.error(f"Error during signal emission spying: {e}")


			# Choose the correct action
			if is_signal_slot:
				# Path for signal-to-signal connections. Must use .emit().
				try:
					slot.emit(*spy_args, **spy_kwargs)
				except Exception as e:
					logging.error(f"Error while emitting chained signal '{slot_name}': {e}")
			else:
				# Path for regular slots
				try:
					return slot(*spy_args, **spy_kwargs)
				except TypeError as e:
					error_str = str(e)
					if "takes" in error_str and "but" in error_str and "were given" in error_str:
						#logging.debug(f"Caught 'too many arguments' TypeError for '{slot_name}'; retrying with no args.")
						try:
							return slot()
						except Exception as e2:
							logging.error(f"Fallback call to '{slot_name}()' also failed: {e2}")
							raise e
					elif "is not connected" in error_str:
						#logging.debug(f"Caught TypeError from '{slot_name}', interpreting as disconnect request.")
						try:
							self.disconnect(spy_wrapper)
							logging.debug(f"[SIGNAL DISCONNECT] Spy for '{slot_name}' fulfilled disconnect request.")
						except TypeError:
							pass
						return
					else:
						raise  # Re-raise other TypeErrors
		
		return original_connect(self, spy_wrapper, *args, **kwargs)

	monkeypatch.setattr(pyqtBoundSignal, "connect", patched_connect)

# endregion
