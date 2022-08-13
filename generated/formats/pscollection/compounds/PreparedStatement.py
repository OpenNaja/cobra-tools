import generated.formats.base.basic
import generated.formats.pscollection.compounds.Arg
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PreparedStatement(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.arg_count = 0
		self.args = ArrayPointer(self.context, self.arg_count, generated.formats.pscollection.compounds.Arg.Arg)
		self.statement_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.sql_query = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.arg_count = 0
		self.args = ArrayPointer(self.context, self.arg_count, generated.formats.pscollection.compounds.Arg.Arg)
		self.statement_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.sql_query = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.args = ArrayPointer.from_stream(stream, instance.context, instance.arg_count, generated.formats.pscollection.compounds.Arg.Arg)
		instance.arg_count = stream.read_uint64()
		instance.statement_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.sql_query = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.args, int):
			instance.args.arg = instance.arg_count
		if not isinstance(instance.statement_name, int):
			instance.statement_name.arg = 0
		if not isinstance(instance.sql_query, int):
			instance.sql_query.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.args)
		stream.write_uint64(instance.arg_count)
		Pointer.to_stream(stream, instance.statement_name)
		Pointer.to_stream(stream, instance.sql_query)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('args', ArrayPointer, (instance.arg_count, generated.formats.pscollection.compounds.Arg.Arg))
		yield ('arg_count', Uint64, (0, None))
		yield ('statement_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('sql_query', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'PreparedStatement [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* args = {self.fmt_member(self.args, indent+1)}'
		s += f'\n	* arg_count = {self.fmt_member(self.arg_count, indent+1)}'
		s += f'\n	* statement_name = {self.fmt_member(self.statement_name, indent+1)}'
		s += f'\n	* sql_query = {self.fmt_member(self.sql_query, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
