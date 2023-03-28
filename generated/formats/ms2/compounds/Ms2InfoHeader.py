from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ms2.basic import BiosynVersion
from generated.formats.ms2.compounds.Buffer0 import Buffer0
from generated.formats.ms2.compounds.BufferInfo import BufferInfo
from generated.formats.ms2.compounds.BufferPresence import BufferPresence
from generated.formats.ms2.compounds.ModelInfo import ModelInfo
from generated.formats.ms2.compounds.ModelReader import ModelReader
from generated.formats.ms2.compounds.Ms2Root import Ms2Root


class Ms2InfoHeader(BaseStruct):

	"""
	Custom header struct
	"""

	__name__ = 'Ms2InfoHeader'

	_import_key = 'ms2.compounds.Ms2InfoHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.biosyn = 0
		self.bone_info_size = 0
		self.num_streams = 0
		self.info = Ms2Root(self.context, 0, None)

		# used since DLA
		self.buffer_pointers = Array(self.context, 0, None, (0,), BufferPresence)
		self.mdl_2_names = Array(self.context, 0, None, (0,), ZString)
		self.modelstream_names = Array(self.context, 0, None, (0,), ZString)
		self.buffer_0 = Buffer0(self.context, self.info, None)
		self.buffer_infos = Array(self.context, 0, None, (0,), BufferInfo)
		self.model_infos = Array(self.context, 0, None, (0,), ModelInfo)

		# handles interleaved (old) or separate (new) styles for models and bone infos
		self.models_reader = ModelReader(self.context, self.model_infos, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('biosyn', BiosynVersion, (0, None), (False, None), (None, None))
		yield ('bone_info_size', Uint, (0, None), (False, None), (None, None))
		yield ('num_streams', Uint, (0, None), (False, None), (None, None))
		yield ('info', Ms2Root, (0, None), (False, None), (None, None))
		yield ('buffer_pointers', Array, (0, None, (None,), BufferPresence), (False, None), (lambda context: context.version >= 7, None))
		yield ('mdl_2_names', Array, (0, None, (None,), ZString), (False, None), (None, None))
		yield ('modelstream_names', Array, (0, None, (None,), ZString), (False, None), (None, None))
		yield ('buffer_0', Buffer0, (None, None), (False, None), (None, None))
		yield ('buffer_infos', Array, (0, None, (None,), BufferInfo), (False, None), (None, None))
		yield ('model_infos', Array, (0, None, (None,), ModelInfo), (False, None), (None, None))
		yield ('models_reader', ModelReader, (None, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'biosyn', BiosynVersion, (0, None), (False, None)
		yield 'bone_info_size', Uint, (0, None), (False, None)
		yield 'num_streams', Uint, (0, None), (False, None)
		yield 'info', Ms2Root, (0, None), (False, None)
		if instance.context.version >= 7:
			yield 'buffer_pointers', Array, (0, None, (instance.info.vertex_buffer_count,), BufferPresence), (False, None)
		yield 'mdl_2_names', Array, (0, None, (instance.info.mdl_2_count,), ZString), (False, None)
		yield 'modelstream_names', Array, (0, None, (instance.num_streams,), ZString), (False, None)
		yield 'buffer_0', Buffer0, (instance.info, None), (False, None)
		yield 'buffer_infos', Array, (0, None, (instance.info.vertex_buffer_count,), BufferInfo), (False, None)
		yield 'model_infos', Array, (0, None, (instance.info.mdl_2_count,), ModelInfo), (False, None)
		yield 'models_reader', ModelReader, (instance.model_infos, None), (False, None)


Ms2InfoHeader.init_attributes()
