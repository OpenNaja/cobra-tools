import logging
import os
import sys
import threading
import time
import platform
from contextlib import contextmanager
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Generator, Any

# --- ANSI and Colored Formatter Classes ---
class ANSI:
	BLACK = "\x1b[0;30m"; RED = "\x1b[0;31m"; GREEN = "\x1b[0;32m"; YELLOW = "\x1b[0;33m"
	BLUE = "\x1b[0;34m"; PURPLE = "\x1b[0;35m"; CYAN = "\x1b[0;36m"; LIGHT_GRAY = "\x1b[0;37m"
	DARK_GRAY = "\x1b[1;30m"; LIGHT_RED = "\x1b[1;31m"; LIGHT_GREEN = "\x1b[1;32m"; LIGHT_YELLOW = "\x1b[1;33m"
	LIGHT_BLUE = "\x1b[1;34m"; LIGHT_PURPLE = "\x1b[1;35m"; LIGHT_CYAN = "\x1b[1;36m"; LIGHT_WHITE = "\x1b[1;37m"
	BOLD = "\x1b[1m"; FAINT = "\x1b[2m"; ITALIC = "\x1b[3m"; UNDERLINE = "\x1b[4m"
	BLINK = "\x1b[5m"; NEGATIVE = "\x1b[7m"; CROSSED = "\x1b[9m"; END = "\x1b[0m"
	if not sys.stdout.isatty() or (platform.system() == "Windows" and platform.release() not in ("10", "11")):
		for _ in dir():
			if isinstance(_, str) and _[0] != "_": locals()[_] = ""
	elif platform.system() == "Windows": os.system("color")

class ColoredFormatter(logging.Formatter):
	def format(self, record):
		formatter = self.FORMATTERS.get(record.levelno)
		return formatter.format(record)

class AnsiFormatter(ColoredFormatter):
	def __init__(self, fmt: str, datefmt: str = None, *args, **kwargs):
		super().__init__(fmt, datefmt, *args, **kwargs)
		self.FORMATS = {
			logging.DEBUG: f"{ANSI.DARK_GRAY}{self._fmt}{ANSI.END}",
			logging.INFO: f"{ANSI.LIGHT_WHITE}{self._fmt}{ANSI.END}",
			logging.INFO + 5: f"{ANSI.LIGHT_GREEN}{self._fmt}{ANSI.END}",
			logging.WARNING: f"{ANSI.YELLOW}{self._fmt}{ANSI.END}",
			logging.ERROR: f"{ANSI.RED}{self._fmt}{ANSI.END}",
			logging.CRITICAL: f"{ANSI.LIGHT_RED}{self._fmt}{ANSI.END}"
		}
		self.FORMATTERS = {key: logging.Formatter(_fmt, datefmt) for key, _fmt in self.FORMATS.items()}


_global_listener: QueueListener | None = None
def get_global_listener() -> QueueListener | None:
	"""
	Returns the application-wide QueueListener instance
	"""
	return _global_listener


# --- Core Components for the Benchmark ---


class DelegatingFormatter(logging.Formatter):
	def __init__(self, initial_formatter: logging.Formatter):
		self._delegate = initial_formatter
		self._lock = threading.Lock()

	def format(self, record: logging.LogRecord) -> str:
		# Check if a temporary formatter was attached to this specific record.
		if hasattr(record, "temporary_formatter"):
			# Use the record-specific formatter.
			return record.temporary_formatter.format(record)
		
		# Otherwise, use the handler's default delegate formatter.
		with self._lock:
			return self._delegate.format(record)

	def set_delegate(self, new_delegate: logging.Formatter):
		with self._lock:
			self._delegate = new_delegate

	@property
	def delegate(self) -> logging.Formatter:
		with self._lock:
			return self._delegate


class TemporaryFormatFilter(logging.Filter):
	def __init__(self, formatter: logging.Formatter):
		super().__init__()
		self.formatter = formatter

	def filter(self, record: logging.LogRecord) -> bool:
		record.temporary_formatter = self.formatter
		return True


@contextmanager
def temporary_formatter(
	formatter: str | logging.Formatter
) -> Generator[None, Any, None]:
	"""
	Thread-safe, race-free context manager that uses a filter to attach a temporary
	formatter directly to LogRecords.
	"""
	if isinstance(formatter, str):
		new_formatter = logging.Formatter(formatter)
	else:
		new_formatter = formatter

	temp_filter = TemporaryFormatFilter(new_formatter)
	logger = logging.getLogger()
	
	try:
		logger.addFilter(temp_filter)
		yield
	finally:
		logger.removeFilter(temp_filter)


def logging_setup(use_delegating_formatter: bool = False) -> tuple[Queue, QueueListener]:
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	colored_formatter = AnsiFormatter('%(levelname)s | %(message)s')
	if use_delegating_formatter:
		final_formatter = DelegatingFormatter(colored_formatter)
	else:
		final_formatter = colored_formatter
	stdout_handler = logging.StreamHandler(sys.stdout)
	stdout_handler.setLevel(logging.DEBUG)
	stdout_handler.setFormatter(final_formatter)
	log_queue = Queue(-1)
	queue_handler = QueueHandler(log_queue)
	if logger.handlers:
		logger.handlers.clear()
	logger.addHandler(queue_handler)
	
	global _global_listener
	_global_listener = QueueListener(log_queue, stdout_handler, respect_handler_level=True)
	_global_listener.start()
	return log_queue

# --- Benchmark Functions ---

def run_benchmark(use_delegating: bool, num_messages: int):
	log_message = "This is a standard test message for the benchmark."
	original_stdout = sys.stdout
	sys.stdout = open(os.devnull, 'w')
	try:
		log_queue = logging_setup(use_delegating_formatter=use_delegating)
		start_time = time.perf_counter()
		for _ in range(num_messages):
			logging.debug(log_message)
		while not log_queue.empty(): time.sleep(0.001)
		_global_listener.stop()
		end_time = time.perf_counter()
	finally:
		sys.stdout.close()
		sys.stdout = original_stdout
		logging.getLogger().handlers.clear()
	return end_time - start_time

def run_block_swap_benchmark(num_messages: int, swap_percentage: float):
	"""
	A benchmark that wraps a single, contiguous block of messages
	in the temporary_formatter, which is a realistic use case.
	"""
	log_message = "This is a standard test message for the benchmark."
	swapped_log_message = "This is a SWAPPED test message."
	swap_formatter = logging.Formatter("[SWAPPED] %(message)s")

	num_swapped = int(num_messages * (swap_percentage / 100.0))
	num_normal = num_messages - num_swapped

	original_stdout = sys.stdout
	sys.stdout = open(os.devnull, 'w')
	try:
		log_queue = logging_setup(use_delegating_formatter=True)
		start_time = time.perf_counter()

		# --- The Swap Block ---
		# The context manager is entered only ONCE for the entire block.
		with temporary_formatter(swap_formatter):
			for _ in range(num_swapped):
				logging.debug(swapped_log_message)

		# --- The Normal Block ---
		# The formatter has now been automatically restored.
		for _ in range(num_normal):
			logging.debug(log_message)

		while not log_queue.empty(): time.sleep(0.001)
		_global_listener.stop()
		end_time = time.perf_counter()
	finally:
		sys.stdout.close()
		sys.stdout = original_stdout
		logging.getLogger().handlers.clear()
	return end_time - start_time

# --- Main Execution Block ---

if __name__ == "__main__":
	NUM_MESSAGES = 100_000
	SWAP_PERCENTAGE = 50.0
	NUM_RUNS = 5

	print(f"--- Starting Logging Benchmark ---")
	print(f"Configuration: {NUM_MESSAGES:,} messages/run, {NUM_RUNS} runs, {SWAP_PERCENTAGE:.1f}% block swap rate.")
	print("NOTE: Logging output is redirected to null to measure pipeline performance.")

	standard_results = []
	delegating_results = []
	block_swap_results = []

	for i in range(NUM_RUNS):
		print(f"\n--- Running Iteration {i + 1}/{NUM_RUNS} ---")

		# Run 1: Standard Formatters
		std_duration = run_benchmark(use_delegating=False, num_messages=NUM_MESSAGES)
		standard_results.append(std_duration)
		print(f"  Standard AnsiFormatter: {std_duration:.4f}s")

		# Run 2: Delegating Formatter (no swapping)
		del_duration = run_benchmark(use_delegating=True, num_messages=NUM_MESSAGES)
		delegating_results.append(del_duration)
		print(f"  Delegating AnsiFormatter: {del_duration:.4f}s")

		# Run 3: Delegating Formatter with a single block swap
		swap_duration = run_block_swap_benchmark(num_messages=NUM_MESSAGES, swap_percentage=SWAP_PERCENTAGE)
		block_swap_results.append(swap_duration)
		print(f"  Delegating with Block Swap: {swap_duration:.4f}s")

	# Calculate averages
	avg_standard = sum(standard_results) / NUM_RUNS
	avg_delegating = sum(delegating_results) / NUM_RUNS
	avg_swap = sum(block_swap_results) / NUM_RUNS

	# Final Comparison based on averages
	print(f"\n--- Benchmark Analysis (Averaged over {NUM_RUNS} runs) ---")
	print(f"Avg Standard Time:   {avg_standard:.4f} seconds")
	print(f"Avg Delegating Time: {avg_delegating:.4f} seconds")
	print(f"Avg Block Swap Time: {avg_swap:.4f} seconds")

	overhead_delegating = avg_delegating - avg_standard
	overhead_swapping = avg_swap - avg_delegating

	if avg_standard > 0:
		percent_delegating = (overhead_delegating / avg_standard) * 100
		print(f"\n1. Overhead of adding DelegatingFormatter wrapper: {overhead_delegating:.4f}s ({percent_delegating:+.2f}%)")

	if avg_delegating > 0:
		percent_swapping = (overhead_swapping / avg_delegating) * 100
		print(f"2. Overhead of using a temporary format for a block of {SWAP_PERCENTAGE:.0f}% of messages: {overhead_swapping:.4f}s ({percent_swapping:+.2f}%)")

