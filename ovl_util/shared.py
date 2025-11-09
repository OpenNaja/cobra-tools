import io
from typing import Any, Generator, LiteralString, Iterable


def check_any(iterable, string):
	"""Returns true if any of the entries of the iterable occur in string"""
	return any([i in string for i in iterable])


TAB = '  '


def hex_dump(data: str | bytes | Iterable[int], show_offset=True, show_txt=True,
			 indent=0, offset=0, line_width=16, encoding="latin-1") -> str:
	"""
	Pretty-prints a sequence in hex dump format.

	Args:
		data: The sequence to be printed.
	"""
	if isinstance(data, str):
		data = bytearray(data, encoding)
	else:
		data = bytearray(data)

	hex_format: LiteralString = " ".join(["{:02X}" for _ in range(line_width)])
	output = io.StringIO()
	for i in range(0, len(data), line_width):
		# Must pad to line width for format string
		line_data: bytearray = data[i:i + line_width].ljust(line_width, b'\x00')
		txt_line: str = ""
		offset_line: str = ""
		# Show text column
		if show_txt:
			for c in line_data:
				c: str = chr(c)
				txt_line += c if c.isprintable() else "."
			txt_line = f"  {txt_line}"
		# Show offset column
		if show_offset:
			offset_line = f"{i + offset:08X}  "
		output.write(f"{indent * TAB}{offset_line}{hex_format.format(*line_data)}{txt_line}\n")
	return output.getvalue()


def hex_dump_generator(in_file: io.BufferedReader, show_offset=True, show_txt=True,
					   indent=0, offset=0, line_width=16) -> Generator[str, Any, None]:
	"""
	Pretty-prints a file in hex dump format.

	Args:
		in_file: A BufferedReader for the input file
	"""
	hex_format: LiteralString = " ".join(["{:02X}" for _ in range(line_width)])
	offset: int = offset
	while True:
		data: bytes = in_file.read(line_width)
		if not data:
			break

		# Must pad to line width for format string
		line_data: bytes = data.ljust(line_width, b'\x00')
		txt_line: str = ""
		offset_line: str = ""
		# Show text column
		if show_txt:
			for c in line_data:
				c: str = chr(c)
				txt_line += c if c.isprintable() else "."
			txt_line = f"  {txt_line}"
		# Show offset column
		if show_offset:
			offset_line = f"{offset:08X}  "
		yield f"{indent * TAB}{offset_line}{hex_format.format(*line_data)}{txt_line}\n"

		offset += line_width

def splitext_safe(fp: str) -> tuple[str, str]:
	# os.path.splitext fails on /ymaiotriqnd03i9/.texel
	name, ext = fp.rsplit(".", 1)
	return name, f".{ext}"