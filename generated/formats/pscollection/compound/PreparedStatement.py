from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.pscollection.compound.Arg
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class PreparedStatement(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.arg_count = 0
		self.args = 0
		self.statement_name = 0
		self.sql_query = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.arg_count = 0
		self.args = ArrayPointer(self.context, self.arg_count, generated.formats.pscollection.compound.Arg.Arg)
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
		instance.args = ArrayPointer.from_stream(stream, instance.context, instance.arg_count, generated.formats.pscollection.compound.Arg.Arg)
		instance.arg_count = stream.read_uint64()
		instance.statement_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.sql_query = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.args.arg = instance.arg_count
		instance.statement_name.arg = 0
		instance.sql_query.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.args)
		stream.write_uint64(instance.arg_count)
		Pointer.to_stream(stream, instance.statement_name)
		Pointer.to_stream(stream, instance.sql_query)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'PreparedStatement [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* args = {fmt_member(self.args, indent+1)}'
		s += f'\n	* arg_count = {fmt_member(self.arg_count, indent+1)}'
		s += f'\n	* statement_name = {fmt_member(self.statement_name, indent+1)}'
		s += f'\n	* sql_query = {fmt_member(self.sql_query, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
