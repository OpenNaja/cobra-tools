from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.imports import name_type_map


class MusicSegment(HircObject):

	__name__ = 'MusicSegment'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.music_node_params = name_type_map['MusicNodeParams'](self.context, 0, None)
		self.f_duration = name_type_map['Double'](self.context, 0, None)
		self.ul_num_markers = name_type_map['Uint'](self.context, 0, None)
		self.markers = Array(self.context, 0, None, (0,), name_type_map['AkMusicMarkerWwise'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'music_node_params', name_type_map['MusicNodeParams'], (0, None), (False, None), (None, None)
		yield 'f_duration', name_type_map['Double'], (0, None), (False, None), (None, None)
		yield 'ul_num_markers', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'markers', Array, (0, None, (None,), name_type_map['AkMusicMarkerWwise']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'music_node_params', name_type_map['MusicNodeParams'], (0, None), (False, None)
		yield 'f_duration', name_type_map['Double'], (0, None), (False, None)
		yield 'ul_num_markers', name_type_map['Uint'], (0, None), (False, None)
		yield 'markers', Array, (0, None, (instance.ul_num_markers,), name_type_map['AkMusicMarkerWwise']), (False, None)
