import logging
import math
import numpy as np

from generated.formats.ms2.compounds.ZtTriBlockInfo import ZtTriBlockInfo
from generated.formats.ms2.compounds.ZtVertBlockInfo import ZtVertBlockInfo
from generated.formats.ms2.compounds.packing_utils import *
from plugin.utils.tristrip import triangulate
from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort
from generated.formats.ms2.bitfields.ModelFlagDLA import ModelFlagDLA
from generated.formats.ms2.bitfields.ModelFlagZT import ModelFlagZT
from generated.formats.ms2.compounds.MeshData import MeshData


class ZtMeshData(MeshData):

	"""
	64 bytes total, same layout for DLA and ZTUAC
	"""

	__name__ = 'ZtMeshData'

	_import_key = 'ms2.compounds.ZtMeshData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# repeat
		self.tri_index_count = 0
		self.vertex_count = 0

		# stores count, -1 as ints
		self.tri_info_offset = 0

		# stores count, -1 as ints
		self.vert_info_offset = 0
		self.known_ff_0 = 0
		self.tri_offset = 0

		# variable dtype, can include vertices too
		self.uv_offset = 0

		# if present, blocks of 24 bytes
		self.vertex_offset = 0
		self.unk_index = 0
		self.one_0 = 0

		# ?
		self.one_1 = 0

		# ?
		self.poweroftwo = 0

		# bitfield
		self.flag = ModelFlagZT(self.context, 0, None)

		# always zero
		self.zero_uac = 0
		if set_default:
			self.set_defaults()

	_attribute_list = MeshData._attribute_list + [
		('tri_index_count', Uint, (0, None), (False, None), None),
		('vertex_count', Uint, (0, None), (False, None), None),
		('tri_info_offset', Uint, (0, None), (False, None), None),
		('vert_info_offset', Uint, (0, None), (False, None), None),
		('known_ff_0', Int, (0, None), (False, None), None),
		('tri_offset', Uint, (0, None), (False, None), None),
		('uv_offset', Uint, (0, None), (False, None), None),
		('vertex_offset', Uint, (0, None), (False, None), None),
		('unk_index', Short, (0, None), (False, None), None),
		('one_0', Ushort, (0, None), (False, None), None),
		('one_1', Ushort, (0, None), (False, None), None),
		('poweroftwo', Ushort, (0, None), (False, None), None),
		('flag', ModelFlagDLA, (0, None), (False, None), True),
		('flag', ModelFlagZT, (0, None), (False, None), True),
		('zero_uac', Uint, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'tri_index_count', Uint, (0, None), (False, None)
		yield 'vertex_count', Uint, (0, None), (False, None)
		yield 'tri_info_offset', Uint, (0, None), (False, None)
		yield 'vert_info_offset', Uint, (0, None), (False, None)
		yield 'known_ff_0', Int, (0, None), (False, None)
		yield 'tri_offset', Uint, (0, None), (False, None)
		yield 'uv_offset', Uint, (0, None), (False, None)
		yield 'vertex_offset', Uint, (0, None), (False, None)
		yield 'unk_index', Short, (0, None), (False, None)
		yield 'one_0', Ushort, (0, None), (False, None)
		yield 'one_1', Ushort, (0, None), (False, None)
		yield 'poweroftwo', Ushort, (0, None), (False, None)
		if instance.context.version <= 7:
			yield 'flag', ModelFlagDLA, (0, None), (False, None)
		if instance.context.version >= 13:
			yield 'flag', ModelFlagZT, (0, None), (False, None)
		yield 'zero_uac', Uint, (0, None), (False, None)

	def init_arrays(self):
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt_colors["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt_colors["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights_info = {}

	def update_dtype(self):
		"""Update MeshData.dt (numpy dtype) according to MeshData.flag"""
		# basic shared stuff
		dt = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
			("pos", np.float16, (3,)),
			("one", np.float16),
			("normal", np.ubyte, (3,)),
			("winding", np.ubyte, ),  # not tested
			("tangent", np.ubyte, (3,)),
			("bone index", np.ubyte, ),  # not tested
		]
		size = self.guess_size(self.buffer_info.uvs_offsets, self.uv_offset, self.vertex_count)
		logging.info(f"Guessed size {size}")
		if 4294967295 == self.vertex_offset:
			if size == 24:
				# 24 bytes per vert, flag is unk
				dt_colors = [
					("pos", np.float16, (3,)),
					("one", np.float16),
					("normal", np.ubyte, (3,)),
					("winding", np.ubyte, ),  # not tested
					("tangent", np.ubyte, (3,)),
					("bone index", np.ubyte, ),  # not tested
					("colors", np.ubyte, (1, 4)),
					("uvs", np.ushort, (1, 2)),
				]
			else:
				# 20 bytes per vert
				dt_colors = [
					("pos", np.float16, (3,)),
					("one", np.float16),
					("normal", np.ubyte, (3,)),
					("winding", np.ubyte, ),  # not tested
					("tangent", np.ubyte, (3,)),
					("bone index", np.ubyte, ),  # not tested
					("uvs", np.ushort, (1, 2)),
				]
		else:
			# hack for zt monitor
			if size == 4:
				dt_colors = [
					("uvs", np.ushort, (1, 2)),
				]
			else:
				dt_colors = [
					("colors", np.ubyte, (1, 4)),
					("uvs", np.ushort, (1 + self.some_index, 2)),
				]
		self.dt = np.dtype(dt)
		self.dt_colors = np.dtype(dt_colors)
		self.update_shell_count()

	def read_verts(self):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# create arrays for the unpacked ms2_file
		self.init_arrays()
		self.buffer_info.verts.seek(self.tri_info_offset)
		tri_info = ZtTriBlockInfo.from_stream(self.buffer_info.verts, self.context, 0, None)
		self.buffer_info.verts.seek(self.vert_info_offset)
		vert_info = ZtVertBlockInfo.from_stream(self.buffer_info.verts, self.context, 0, None)
		# logging.info(self)
		# logging.info(tri_info)
		# logging.info(vert_info)
		# read vertices of this mesh
		self.verts_data = np.empty(dtype=self.dt, shape=self.vertex_count)
		self.colors_data = np.empty(dtype=self.dt_colors, shape=self.vertex_count)
		self.buffer_info.uvs.seek(self.uv_offset)
		# logging.debug(f"UV at {self.buffer_info.uvs.tell()}")
		self.buffer_info.uvs.readinto(self.colors_data)
		if 4294967295 != self.vertex_offset:
			self.buffer_info.verts.seek(self.vertex_offset)
			# logging.debug(f"{self.vertex_count} VERTS at {self.buffer_info.verts.tell()}")
			self.buffer_info.verts.readinto(self.verts_data)
			self.normals[:] = self.verts_data["normal"]
			self.tangents[:] = self.verts_data["tangent"]
			self.vertices[:] = self.verts_data["pos"]

			# if "bone weights" in self.dt.fields:
			bone_weights = self.verts_data["bone weights"].astype(np.float32) / 255
			self.get_blended_weights(self.verts_data["bone ids"], bone_weights)
		else:
			self.normals[:] = self.colors_data["normal"]
			self.tangents[:] = self.colors_data["tangent"]
			self.vertices[:] = self.colors_data["pos"]

		# first cast to the float uvs array so unpacking doesn't use int division
		if self.colors is not None:
			# first cast to the float colors array so unpacking doesn't use int division
			self.colors[:] = self.colors_data["colors"]
			unpack_ubyte_color(self.colors)
		if self.uvs is not None:
			self.uvs[:] = self.colors_data["uvs"]
			self.uvs /= 2048
		unpack_ubyte_vector(self.normals)
		unpack_ubyte_vector(self.tangents)
		unpack_swizzle_vectorized(self.vertices)
		unpack_swizzle_vectorized_b(self.normals)
		unpack_swizzle_vectorized(self.tangents)

		# self.get_static_weights(self.verts_data["bone index"], self.use_blended_weights)


