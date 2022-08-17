from enum import EnumMeta, IntEnum


# https://stackoverflow.com/questions/44867597/is-there-a-way-to-specify-a-default-value-for-python-enums
class DefaultEnumMeta(EnumMeta):
	default = object()

	def __call__(cls, *args, value=default, **kwargs):
		if value is DefaultEnumMeta.default:
			# Assume the first enum is default
			return next(iter(cls))
		return super().__call__(value, *args, **kwargs)

	# Execute base __new__ https://github.com/python/cpython/blob/32959108f9c543e3cb9f2b68bbc782bddded6f42/Lib/enum.py#L410
	# and then move __new__ to from_value, while the new __new__ accepts the standardized arguments
	def __new__(metacls, *args, **kwargs):
		enum_class = super(metacls, metacls).__new__(metacls, *args, **kwargs)
		new_function = enum_class.__new__
		# from_value doesn't need to be a proper __new__-like function, because specified enums can't be inherited from
		enum_class.from_value = classmethod(lambda cls, value: new_function(cls, value))
		enum_class.__new__ = lambda cls, context=None, arg=0, template=None, set_default=True: new_function(cls)
		return enum_class


class BaseEnum(IntEnum, metaclass=DefaultEnumMeta):

	def __int__(self):
		return self.value
	pass

	@classmethod
	def from_str(cls, label):
		"""Creates the enum from its str representation"""
		assert "." in label
		value = label.split(".")[-1]
		try:
			enum = cls[value]
		except KeyError:
			raise KeyError(f"Key '{value}' not found in enum '{cls.__name__}', outdated definition?")
		return enum

	@classmethod
	def from_xml(cls, target, elem, prop, arguments=None):
		return cls.from_str(elem.attrib[prop])

	@classmethod
	def to_xml(cls, elem, prop, instance, arguments, debug):
		elem.attrib[prop] = str(instance)
