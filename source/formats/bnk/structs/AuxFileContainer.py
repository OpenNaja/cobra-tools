import io
import logging
import os

from generated.formats.base.basic import Uint
from generated.formats.bnk.structs.BKHDSection import BKHDSection
from generated.formats.bnk.structs.DATASection import DATASection
from generated.formats.bnk.structs.DIDXSection import DIDXSection
from generated.formats.bnk.structs.HIRCSection import HIRCSection
from generated.base_struct import BaseStruct
from generated.formats.base.structs.PadAlign import get_padding
from generated.formats.bnk.enums.HircType import HircType
from modules.formats.shared import fmt_hash


class AuxFileContainer(BaseStruct):
	# Custom file struct

	def __init__(self, context, arg=0, template=None, set_default=False):
		super().__init__(context, arg, template, set_default=False)
		self.chunks = []
		self.bhkd = None
		self.didx = None
		self.hirc = None
		self.data = None
		self.size_for_ovl = 0

	@classmethod
	def read_fields(cls, stream, instance):
		try:
			instance.chunks = []
			chunk_id = "DUMM"
			while len(chunk_id) == 4:
				chunk_id = stream.read(4)
				after_size_pos = stream.tell() + 4
				logging.debug(f"reading chunk {chunk_id} at {stream.tell()}")
				logging.debug(f"version={instance.context.version}")
				if chunk_id == b"BKHD":
					instance.bhkd = BKHDSection.from_stream(stream, instance.context, 0, None)
					# print(instance.bhkd)
					instance.chunks.append((chunk_id, instance.bhkd))
				elif chunk_id == b"HIRC":
					instance.hirc = HIRCSection.from_stream(stream, instance.context, 0, None)
					# print(instance.hirc)
					instance.chunks.append((chunk_id, instance.hirc))
				elif chunk_id == b"DIDX":
					instance.didx = DIDXSection.from_stream(stream, instance.context, 0, None)
					instance.chunks.append((chunk_id, instance.didx))
				elif chunk_id == b"DATA":
					instance.data = DATASection.from_stream(stream, instance.context, 0, None)
					instance.chunks.append((chunk_id, instance.data))
				elif chunk_id == b'\x00' * len(chunk_id):
					# empty chunk, could be the end of the file
					break
				else:
					raise NotImplementedError(f"Unknown chunk {chunk_id}!")
				# see where this chunk should have ended
				desired_end = after_size_pos + instance.chunks[-1][1].length
				if stream.tell() != desired_end:
					logging.info(f"Chunk {chunk_id} ended up at bad offset {stream.tell()}, seeking to desired {desired_end}")
					stream.seek(desired_end)
			# id the pointers
			if instance.hirc:
				for pointer in instance.hirc.hirc_pointers:
					if pointer.id == HircType.SOUND:
						pointer.hash = fmt_hash(pointer.data.ak_bank_source_data.ak_media_information.source_i_d)
			if instance.didx:
				for pointer in instance.didx.data_pointers:
					pointer.data = bytes(instance.data.wem_datas[pointer.data_section_offset: pointer.data_section_offset + pointer.wem_filesize])
					pointer.hash = fmt_hash(pointer.wem_id)
					# logging.debug(f"Pointer {pointer.hash} has {pointer.data_section_offset} bytes {pointer.wem_filesize}")
		except:
			raise

	def inject_audio(self, wem_path, wem_id):
		"""Loads wem audio into the container"""
		logging.info(f"Injecting audio for {wem_id}")
		for pointer in self.didx.data_pointers:
			if pointer.hash == wem_id:
				logging.info(f"found a match {pointer.hash}, injecting audio")
				# logging.info(f"{pointer.hash} before injection - {len(pointer.data)} bytes, reading wem data")
				with open(wem_path, "rb") as f:
					pointer.data = f.read()
				pointer.wem_filesize = len(pointer.data)
				# logging.info(f"{pointer.hash} after injection - {len(pointer.data)} bytes")
				break

	def inject_hirc(self, wem_path, wem_id):
		"""Loads wem size into the events container"""
		logging.info(f"Updating hirc data size for {wem_id}")
		if self.hirc:
			for pointer in self.hirc.hirc_pointers:
				if pointer.id == HircType.SOUND:
					if pointer.hash == wem_id:
						logging.debug(f"found a match {pointer.hash}, updating wem data size")
						bank = pointer.data.ak_bank_source_data
						bank.size = bank.ak_media_information.u_in_memory_media_size = os.path.getsize(wem_path)
						break

	def __repr__(self):
		s = 'AuxFileContainer'
		for chunk in self.chunks:
			s += '\nchunk ' + chunk.__repr__()
		s += '\n'
		return s

	@classmethod
	def write_fields(cls, stream, instance):
		"""Update representation, then write the container from the internal representation"""
		if instance.didx:
			# update didx pointers and build data bytes
			with io.BytesIO() as f:
				for pointer in instance.didx.data_pointers:
					# offset must be aligned to 16
					f.write(get_padding(f.tell(), alignment=16))
					logging.info(f"before {pointer.data_section_offset}")
					pointer.data_section_offset = f.tell()
					logging.info(f"after  {pointer.data_section_offset}")
					f.write(pointer.data)
				data = f.getvalue()

		for chunk_id, chunk in instance.chunks:
			if chunk_id == b"DATA":
				stream.write(b"DATA")
				# ovl ignores the padding of the last wem
				data_size = len(data)
				instance.size_for_ovl = stream.tell() + data_size
				Uint.to_stream(data_size, stream)
				stream.write(data)
			else:
				# print(stream.tell(), chunk_id, chunk)
				stream.write(chunk_id)
				chunk.to_stream(chunk, stream, instance.context)
		if instance.hirc:
			# logging.info(f"End of HIRC at {stream.tell()}")
			pass
		instance.size_for_ovl = stream.tell()
		stream.write(get_padding(stream.tell(), alignment=16))

