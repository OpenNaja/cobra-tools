import logging
import time
import traceback
from pytestqt.wait_signal import MultiSignalBlocker
from typing import Callable


def waitDiagnostic(ms: int) -> None:
	"""
	Waits for a specific amount of time, with detailed logging.
	"""
	# Capture and log the current call stack to see what led to this wait.
	stack_info = ''.join(traceback.format_stack())
	logging.debug(f"Entering wait(ms={ms})...\n--- Call Stack ---\n{stack_info}")

	blocker = MultiSignalBlocker(timeout=ms, raising=False)
	blocker_details = format_blocker_state(blocker)
	logging.debug(f"Created MultiSignalBlocker instance:\n{blocker_details}")

	logging.debug("About to call blocker.wait()")
	blocker.wait()
	logging.debug("Returned from blocker.wait()")

	logging.debug(f"Exiting wait(ms={ms}).")


def waitUntilDiagnostic(callback: Callable[[], bool | None], *, timeout: int = 5000) -> None:
	"""
	Waits until a callback returns a truthy value or raises an AssertionError,
	with detailed logging.
	"""
	start_stack = ''.join(traceback.format_stack())
	logging.debug(
		f"Entering waitUntil(callback={getattr(callback, '__name__', 'N/A')}, timeout={timeout})...\n"
		f"--- Initial Call Stack ---\n{start_stack}"
	)

	start_time = time.time()
	iteration = 0

	def timed_out():
		elapsed_ms = (time.time() - start_time) * 1000
		is_timeout = elapsed_ms > timeout
		if is_timeout:
			logging.warning(f"Timeout check: elapsed_ms ({elapsed_ms:.2f}) > timeout ({timeout}) -> TIMED OUT")
		return is_timeout

	timeout_msg = f"waitUntil timed out in {timeout} milliseconds for callback '{getattr(callback, '__name__', 'N/A')}'"

	while True:
		iteration += 1
		logging.debug(f"--- waitUntil iteration #{iteration} ---")

		# Log the stack right before executing the user's callback.
		# This is often the most critical log entry before a crash.
		current_stack = ''.join(traceback.format_stack())
		logging.debug(f"About to call callback '{getattr(callback, '__name__', 'N/A')}'...\n--- Current Stack ---\n{current_stack}")

		try:
			result = callback()
			logging.debug(f"Callback '{getattr(callback, '__name__', 'N/A')}' returned: {result} (type: {type(result)})")
		except AssertionError as e:
			logging.warning(f"Callback '{getattr(callback, '__name__', 'N/A')}' raised AssertionError: {e}")
			if timed_out():
				logging.error(f"Timeout occurred after AssertionError. Raising TimeoutError.")
				raise TimeoutError(timeout_msg) from e
			logging.debug("Assertion failed, but not timed out yet. Continuing loop.")
		except Exception:
			# Catching other exceptions is useful, as the access violation might
			# be triggered by an unexpected error.
			logging.exception(f"Callback '{getattr(callback, '__name__', 'N/A')}' raised an unexpected exception!")
			if timed_out():
				logging.error(f"Timeout occurred after unexpected exception. Raising TimeoutError.")
				raise TimeoutError(timeout_msg) from e
			logging.debug("Unexpected exception, but not timed out yet. Continuing loop.")
		else:
			if result not in (None, True, False):
				msg = f"waitUntil() callback must return None, True or False, but returned {result!r}"
				logging.error(msg)
				raise ValueError(msg)

			# 'assert' form: successful if it returns None (no assertion failed)
			if result is None:
				logging.info("Callback returned None. Assuming success. Exiting waitUntil.")
				return

			# 'True/False' form
			if result:
				logging.info("Callback returned True. Condition met. Exiting waitUntil.")
				return

			# If result is False, check for timeout before continuing
			if timed_out():
				logging.error(timeout_msg)
				raise TimeoutError(timeout_msg)

		logging.debug("Condition not met and not timed out. Waiting for the next cycle.")
		# Uses the diagnostic 'wait' function for the delay
		waitDiagnostic(10)


def format_blocker_state(blocker: MultiSignalBlocker) -> str:
	"""
	Inspects a MultiSignalBlocker instance and returns a formatted string of its state.
	"""
	# List of attributes to inspect on the blocker instance
	attrs_to_check = [
		"_order",
		"_check_params_callbacks",
		"_signals_emitted",
		"_signals_map",
		"_signals",
		"_slots",
		"_signal_expected_index",
		"_strict_order_violated",
		"_actual_signal_and_args_at_violation",
		"_signal_names",
		"all_signals_and_args",
		"_timeout",
		"_raising",
	]

	header = f"<{blocker.__class__.__name__} instance at {hex(id(blocker))}>"
	state_lines = [header]

	for attr in attrs_to_check:
		# Use getattr for safe access; returns 'N/A' if an attribute doesn't exist
		value = getattr(blocker, attr, "N/A (Attribute not found)")
		state_lines.append(f"  - {attr}: {value!r}")

	return "\n".join(state_lines)
