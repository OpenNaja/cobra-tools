import logging
import pytest
from pytest import MonkeyPatch, FixtureRequest


def pytest_configure(config: pytest.Config) -> None:
	"""Register custom markers."""
	config.addinivalue_line(
		"markers", "trace_qtimer(immediate, threshold): Configure the QTimer tracing fixture."
	)
	config.addinivalue_line(
		"markers", "trace_signal(ignore): Configure the pyqtSignal tracing fixture."
	)


import time
@pytest.fixture(autouse=False)  # Only use for debugging
def slow_down_tests():
	yield
	time.sleep(0.5)


# -------------------------------------------------------------------------- #
#                             TEST ENV GUARDS                                #
# region ------------------------------------------------------------------- #

@pytest.fixture(autouse=True)
def _patch_gui_startup(monkeypatch):
	"""
	Automatically patches gui.startup() for every test.
	
	If any test code accidentally calls gui.startup(), this patch
	will intercept it, log a critical error, and raise an exception
	to fail the test immediately.
	"""
	def _banned_gui_startup(*args, **kwargs):
		"""The function that replaces gui.startup()."""
		error_msg = (
			"FATAL TEST ERROR: gui.startup() was called during a test. "
			"Tests must never call the main application entry point. "
			"Instead, use the 'qapp' fixture and call 'setup_app()' directly."
		)
		logging.critical(error_msg)
		raise RuntimeError(error_msg)

	try:
		monkeypatch.setattr("gui.startup", _banned_gui_startup)
	except ImportError:
		logging.warning("Could not patch gui.startup. Module not found.")
		pass

# endregion

# -------------------------------------------------------------------------- #
#                            LOGGING FIXTURES                                #
# region ------------------------------------------------------------------- #

from gui.widgets.logger import LoggerWidget
@pytest.fixture(autouse=True)
def _patch_gui_logger_for_all_gui_tests(monkeypatch: MonkeyPatch):
	"""
	An autouse fixture that automatically disables the GUI's internal logging
	handler.
	"""
	from gui.widgets.window import MainWindow
	# Patch the GUI's own logging handler to do nothing.
	monkeypatch.setattr(LoggerWidget.Handler, "emit", lambda *args, **kwargs: None)
	
	#monkeypatch.setattr(MainWindow, "perform_initial_layout", lambda *args, **kwargs: None)
	yield



@pytest.fixture(scope="function", autouse=True)
def _bypass_app_logging_setup_for_session(monkeypatch: MonkeyPatch):
	"""
	An autouse fixture to bypass the applications' internal logging setup and teardown.
	"""
	print("\n--- Bypassing application logging setup ---")

	# Null the main logging setup function
	monkeypatch.setattr("ovl_util.logs.logging_setup", lambda *args, **kwargs: None)

	yield

# endregion


# -------------------------------------------------------------------------- #
#                          THREADING/MP FIXTURES                             #
# region ------------------------------------------------------------------- #

@pytest.fixture  # Only for specific test cases, autouse _sync* instead
def _prevent_threads_batch(monkeypatch: MonkeyPatch):
	"""
	A fixture that completely prevents the MainWindow batch logic
	"""
	from gui.widgets.window import MainWindow
	# Replace the method with a function that does nothing
	monkeypatch.setattr(MainWindow, "run_in_threadpool", lambda *args, **kwargs: None)
	yield


@pytest.fixture  # Only for specific test cases, autouse _sync* isntead
def _prevent_threads_background(monkeypatch: MonkeyPatch):
	"""
	A fixture that completely prevents the MainWindow background logic
	"""
	from gui.widgets.window import MainWindow
	# Replace the method with a function that does nothing
	monkeypatch.setattr(MainWindow, "run_background_task", lambda *args, **kwargs: None)
	yield


@pytest.fixture(autouse=True)
def _prevent_worker_cancellation(monkeypatch: MonkeyPatch):
	"""
	An autouse fixture that prevents the MainWindow from trying to cancel
	worker threads during teardown.

	This complements the '_sync'/'_prevent' fixtures. Since those fixtures stop
	threads from being created in the first place, this patch disables the
	redundant cancellation logic.
	"""
	from gui.widgets.window import MainWindow
	# Replace the method with a function that does nothing.
	monkeypatch.setattr(MainWindow, "cancel_workers", lambda *args, **kwargs: None)
	yield


@pytest.fixture(autouse=True)
def _sync_threads_batch(monkeypatch: MonkeyPatch):
	"""
	A fixture that makes run_in_threadpool execute synchronously.
	"""
	from gui.widgets.window import MainWindow

	def synchronous_run_in_threadpool(self, func, callbacks=(), *args, **kwargs):
		# Pop off 'func' and call it with the rest of the args
		func(*args, **kwargs)
		# Mimic the 'finished' signal
		for callback in callbacks:
			callback()

	monkeypatch.setattr(MainWindow, "run_in_threadpool", synchronous_run_in_threadpool)
	yield


@pytest.fixture(autouse=True)
def _sync_threads_background(monkeypatch: MonkeyPatch):
	"""
	A fixture that makes run_background_task execute synchronously.
	"""
	from gui.widgets.window import MainWindow

	class MockWorker:
		"""A fake worker that has a 'cancel' method to prevent exceptions"""
		def cancel(self):
			pass

	def synchronous_run_background_task(self, func, on_result, *args, **kwargs):
		# Pop off 'func' and call it, capturing the result
		result = func(*args, **kwargs, cancellation_check=lambda: False)
		# Mimic the 'result' signal by calling the on_result callback
		on_result(result)
		# The original returns a WorkerRunnable
		return MockWorker()

	monkeypatch.setattr(MainWindow, "run_background_task", synchronous_run_background_task)
	yield

# endregion


# -------------------------------------------------------------------------- #
#                        SESSION GARBAGE COLLECTION                          #
# region ------------------------------------------------------------------- #

from constants import ConstantsProvider
@pytest.fixture(scope="session", autouse=True)
def _prime_constants_cache_for_session():
	"""
	A session-scoped fixture to ensure the massive constants dictionary
	is loaded only once at the beginning of the test session and is held in memory
	until the very end.

	This prevents the heavy garbage collection of the constants from interfering
	with the teardown of individual tests.
	"""
	print("\n--- Pre-loading constants for the entire test session ---")
	
	# This calls your ConstantsProvider, which does the heavy 5-second load
	# and populates the lru_cache.
	constants = ConstantsProvider()
	
	# Yield the object. Pytest will hold a strong reference to it
	# for the duration of the session.
	yield constants
	
	print("\n--- Test session finished, releasing constants for final GC ---")

# endregion


# -------------------------------------------------------------------------- #
#                         DIAGNOSTICS & DEBUGGING                            #
# region ------------------------------------------------------------------- #

# --- MASTER SWITCH FOR QTIMER DEBUGGING ---
# To enable QTimer tracing for ALL tests during development, change the values here.
# A marker on a test function (@pytest.mark.trace_qtimer) will always override these defaults.
_QTIMER_DEFAULT_CONFIG = {
	"autouse": False,			# Set to True to run this fixture for all tests
	"immediate": True,			# Default for 'immediate' when autouse is True
	"threshold": 0,				# Default for 'threshold' when autouse is True
}

@pytest.fixture(autouse=_QTIMER_DEFAULT_CONFIG["autouse"])
def trace_qtimer(monkeypatch: MonkeyPatch, request: FixtureRequest):
	"""
	A configurable fixture to monkeypatch QTimer for debugging.

	Can be enabled globally by editing `_DEFAULT_CONFIG` in this file,
	or on a per-test basis using the 'trace_qtimer' marker. A marker
	will always override the global default settings.

	Marker Usage:
	  - @pytest.mark.trace_qtimer
	  - @pytest.mark.trace_qtimer(immediate=True, threshold=10)
	"""
	from contextlib import nullcontext
	from gui.tools.qt_debug import _trace_qtimer_calls, immediate_singleshot_timers, DebugState
	
	marker = request.node.get_closest_marker("trace_qtimer")
	
	# Default to a context manager that does nothing
	context_manager = nullcontext()

	if marker or _QTIMER_DEFAULT_CONFIG["autouse"]:
		# --- Configuration Phase ---
		use_immediate = False
		threshold = -1

		if marker:
			use_immediate = marker.kwargs.get("immediate", True)
			if use_immediate:
				threshold = marker.kwargs.get("threshold", threshold)
		elif _QTIMER_DEFAULT_CONFIG["autouse"]:
			use_immediate = _QTIMER_DEFAULT_CONFIG["immediate"]
			if use_immediate:
				threshold = _QTIMER_DEFAULT_CONFIG["threshold"]

		# --- Setup Phase ---
		DebugState.qtimer_ignore_patterns.add("_timer")
		_trace_qtimer_calls(monkeypatch, request)

		# --- Context Manager Selection ---
		if use_immediate:
			context_manager = immediate_singleshot_timers(threshold=threshold)

	# --- Execution Phase ---
	with context_manager:
		yield  # The yield must happen regardless of activation to satisfy any dependent fixtures


# --- MASTER SWITCH FOR SIGNAL DEBUGGING ---
_SIGNAL_DEFAULT_CONFIG = {
	"autouse": False,			# Set to True to run this fixture for all tests
	"ignore": [],				# Default ignore list when autouse is True
}

@pytest.fixture(autouse=_SIGNAL_DEFAULT_CONFIG["autouse"])
def trace_signal(monkeypatch: MonkeyPatch, request: FixtureRequest, trace_qtimer: None):
	"""
	A configurable fixture to monkeypatch pyqtSignal.connect for debugging.

	Can be enabled globally by editing `_SIGNAL_DEFAULT_CONFIG` in this file,
	or on a per-test basis using the 'trace_signal' marker.

	Marker Usage:
	  - @pytest.mark.trace_signal
	  - @pytest.mark.trace_signal(ignore=["ClassName.signalName"])
	"""
	from gui.tools.qt_debug import _trace_pyqt_signals, _recompile_signal_ignore_regex, DebugState

	marker = request.node.get_closest_marker("trace_signal")
	if marker or _SIGNAL_DEFAULT_CONFIG["autouse"]:
		# --- Configuration Phase ---
		new_ignores = set()
		if marker:
			# Precedence to test markers
			marker_ignores = marker.kwargs.get("ignore")
			if marker_ignores:
				new_ignores.update(marker_ignores)
		elif _SIGNAL_DEFAULT_CONFIG["autouse"]:
			# Fall back to the global default config
			default_ignores = _SIGNAL_DEFAULT_CONFIG.get("ignore")
			if default_ignores:
				new_ignores.update(default_ignores)

		# --- Setup Phase ---
		if new_ignores:
			DebugState.signal_ignore_patterns.update(new_ignores)

		# Only apply the patch once, but recompile the regex if new patterns were added.
		if not DebugState.signal_debug_active:
			# First-time activation: compile all patterns and apply the patch.
			_recompile_signal_ignore_regex()
			_trace_pyqt_signals(monkeypatch, request)
			DebugState.signal_debug_active = True
		elif new_ignores:
			# Already active, but we added new patterns, so just recompile.
			_recompile_signal_ignore_regex()

	# The yield must happen regardless of activation to satisfy any dependent fixtures
	yield


import tracemalloc

@pytest.fixture(scope="function", autouse=True)
def memory_leak_detector(request: FixtureRequest):
    """
    Activates tracemalloc to detect memory leaks for each test.
    """
    if not request.config.getoption("--tracemalloc"):
        yield
        return

    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()

    yield

    snapshot_after = tracemalloc.take_snapshot()
    tracemalloc.stop()

    # Filter out noise from the testing framework and standard libraries
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
    filters = [
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<frozen importlib._bootstrap_external>"),
        tracemalloc.Filter(False, "<frozen ntpath>"),
        tracemalloc.Filter(False, str(pytest.__file__)),
    ]
    top_stats = snapshot_after.filter_traces(filters).compare_to(snapshot_before.filter_traces(filters), 'lineno')

    if top_stats:
        logging.info(f"--- MEMORY LEAK REPORT for {request.node.name} ---")
        total_leaked = sum(stat.size for stat in top_stats) / 1024
        logging.info(f"Total memory leaked: {total_leaked:.2f} KiB")
        logging.info("Top 10 lines responsible for memory growth:")
        for index, stat in enumerate(top_stats[:10], 1):
            logging.info(f"  {index}: {stat}")
    else:
        logging.info(f"--- MEMORY LEAK REPORT for {request.node.name} ---")
        logging.info("No memory leaks detected.")

# endregion
