# START_GLOBALS
ZERO = b"\x00"
# TODO get rid of these
_b = b''
_b00 = b'\x00'

def _as_bytes(value):
	"""Helper function which converts a string to bytes (this is useful for
	set_value in all string classes, which use bytes for representation).
	:return: The bytes representing the value.
	:rtype: C{bytes}
	>>> _as_bytes("\\u00e9defa") == "\\u00e9defa".encode("utf-8")
	True
	>>> _as_bytes(123) # doctest: +ELLIPSIS
	Traceback (most recent call last):
		...
	TypeError: ...
	"""
	if isinstance(value, str):
		return value.encode("utf-8", "replace")
	elif isinstance(value, bytes):
		return value
	else:
		raise TypeError("expected str")

def _as_str(value):
	"""Helper function to convert bytes back to str. This is used in
	the __str__ functions for simple string types. If you want a custom
	encoding, use an explicit decode call on the value.
	"""
	if isinstance(value, bytes):
		return value.decode("utf-8", "replace")
	elif isinstance(value, str):
		return value
	else:
		raise TypeError("expected bytes")

# END_GLOBALS

class ZString:
	"""Holds a zero-terminated string"""

# START_CLASS

	_maxlen = 1000  #: The maximum length.

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self._value = b''

	def __str__(self):
		return _as_str(self._value)

	def __repr__(self):
		return f"ZString: '{_as_str(self._value)}'"

	def get_value(self):
		"""Return the string.
			:return: The stored string.
			:rtype: C{bytes}
			"""
		return _as_str(self._value)


	def set_value(self, value):
		"""Set string to C{value}.
			:param value: The value to assign.
			:type value: ``str`` (will be encoded as default) or C{bytes}
			"""
		val = _as_bytes(value)
		i = val.find(b'\x00')
		if i != -1:
			val = val[:i]
		if len(val) > self._maxlen:
			raise ValueError('string too long')
		self._value = val


	def read(self, stream, data=None):
		"""Read string from stream.
			:param stream: The stream to read from.
			:type stream: file
			"""
		i = 0
		val = b''
		char = b''
		while char != b'\x00':
			i += 1
			if i > self._maxlen:
				raise ValueError('string too long')
			val += char
			char = stream.read(1)
		self._value = val


	def write(self, stream, data=None):
		"""Write string to stream.
			:param stream: The stream to write to.
			:type stream: file
			"""
		stream.write(self._value)
		stream.write(b'\x00')


	def get_size(self, data=None):
		"""Return number of bytes this type occupies in a file.
			:return: Number of bytes.
			"""
		return len(self._value) + 1


	def get_hash(self, data=None):
		"""Return a hash value for this string.
			:return: An immutable object that can be used as a hash.
			"""
		return self._value
