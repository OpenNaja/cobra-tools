import logging
import os
import struct

from generated.context import ContextReference
from generated.formats.bnk.compound.BKHDSection import BKHDSection
from generated.formats.bnk.compound.DATASection import DATASection
from generated.formats.bnk.compound.DIDXSection import DIDXSection
from generated.formats.bnk.compound.HIRCSection import HIRCSection
from modules.formats.shared import get_padding


class AuxFileContainer:
    # Custom file struct

    context = ContextReference()

    def __init__(self, context, arg=0, template=None, set_default=False):
        self._context = context
        self.arg = arg
        self.template = template
        self.chunks = []
        self.bhkd = None
        self.didx = None
        self.hirc = None
        self.data = None
        self.size_for_ovl = 0
        self.old_size = 0

    def read(self, stream):
        self.read_fields(stream, instance)

    @classmethod
    def read_fields(cls, stream, instance):
        instance.chunks = []
        chunk_id = "DUMM"
        while len(chunk_id) == 4:
            chunk_id = stream.read(4)
            after_size_pos = stream.tell() + 4
            logging.info(f"reading chunk {chunk_id} at {stream.tell()}")
            if chunk_id == b"BKHD":
<<<<<<< HEAD
                self.bhkd = stream.read_type(BKHDSection, (self.context,))
                # print(self.bhkd)
                self.chunks.append((chunk_id, self.bhkd))
=======
                instance.bhkd = BKHDSection.from_stream(stream, instance.context)
                print(instance.bhkd)
                instance.chunks.append((chunk_id, instance.bhkd))
>>>>>>> 693ff8b... Finished finalizing generalized interface.
            elif chunk_id == b"HIRC":
                instance.hirc = HIRCSection.from_stream(stream, instance.context)
                instance.chunks.append((chunk_id, instance.hirc))
            elif chunk_id == b"DIDX":
                instance.didx = DIDX.from_stream(stream, instance.context)
                instance.chunks.append((chunk_id, instance.didx))
            elif chunk_id == b"DATA":
<<<<<<< HEAD
                self.data = stream.read_type(DATASection, (self.context,))
                self.chunks.append((chunk_id, self.data))
            elif chunk_id == b'\x00' * len(chunk_id):
                # empty chunk, could be end
                break
            else:
                raise NotImplementedError(f"Unknown chunk {chunk_id}!")
            desired_end = after_size_pos + self.chunks[-1][1].length
            if stream.tell() != desired_end:
                logging.info(f"Seeking to {desired_end}")
                stream.seek(desired_end)
        # if not self.hirc:
        if self.didx:
            for pointer in self.didx.data_pointers:
                pointer.data = bytes(self.data.wem_datas[
                               pointer.data_section_offset: pointer.data_section_offset + pointer.wem_filesize])
=======
                size = stream.read_uint()
                instance.data = stream.read(size)
            elif chunk_id == b'\x00\x00\x00\x00':
                break
            elif chunk_id == b'\x00':
                break
            elif not chunk_id:
                break
            else:
                raise NotImplementedError(f"Unknown chunk {chunk_id}!")
        # if not instance.hirc:
        if instance.didx:
            for pointer in instance.didx.data_pointers:
                pointer.data = instance.data[
                               pointer.data_section_offset: pointer.data_section_offset + pointer.wem_filesize]
>>>>>>> 693ff8b... Finished finalizing generalized interface.
                pointer.hash = "".join([f"{b:02X}" for b in struct.pack("<I", pointer.wem_id)])
                pointer.pad = b""

    def extract_audio(self, out_dir_func, basename):
        """Extracts all wem files from the container into a folder"""
        print("Extracting audio")
        paths = []
        if self.didx:
            for pointer in self.didx.data_pointers:
                wem_name = f"{basename}_{pointer.hash}.wem"
                wem_path = out_dir_func(wem_name)
                paths.append(wem_path)
                print(wem_path)
                with open(wem_path, "wb") as f:
                    f.write(pointer.data)
        return paths

    def inject_audio(self, wem_path, wem_id):
        """Loads wem audio into the container"""
        print("Injecting audio")
        for pointer in self.didx.data_pointers:
            if pointer.hash == wem_id:
                print("found a match, reading wem data")
                with open(wem_path, "rb") as f:
                    pointer.data = f.read()
                break

    def inject_hirc(self, wem_path, wem_id):
        """Loads wem size into the events container"""
        print("updating hirc data size")
        for hirc_pointer in self.hirc.hirc_pointers:

            if hirc_pointer.id == 2:
                hash = "".join([f"{b:02X}" for b in struct.pack("<I", hirc_pointer.data.didx_id)])
                print(hirc_pointer.id, hash, wem_id)
                if hash == wem_id:
                    print("found a match, reading wem data size")
                    hirc_pointer.data.wem_length = os.path.getsize(wem_path)
                    print(hirc_pointer.data)
                    break

    # if self.hirc != None:
    #   for hirc_pointer in self.hirc.hirc_pointers:
    #      if hirc_pointer.id == 2:

    def write(self, stream):
        self.write_fields(stream, self)

    def __repr__(self):
        s = 'AuxFileContainer'
        for chunk in self.chunks:
            s += '\nchunk ' + chunk.__repr__()
        s += '\n'
        return s

    @classmethod
    def write_fields(cls, stream, instance):
        """Update representation, then write the container from the internal representation"""
        offset = 0
        if not instance.hirc:
            for pointer in instance.didx.data_pointers:
                pointer.data_section_offset = offset
                pointer.wem_filesize = len(pointer.data)
                pointer.pad = get_padding(len(pointer.data), alignment=16)
                offset += len(pointer.data + pointer.pad)
        for chunk_id, chunk in instance.chunks:
            stream.write(chunk_id)
            type(chunk).to_stream(stream, chunk)
        if instance.hirc:
            stream.write(bytearray(instance.old_size - stream.tell()))
            print(stream.tell)
            return
        if not instance.didx.data_pointers:
            return
        data = b"".join(pointer.data + pointer.pad for pointer in instance.didx.data_pointers)
        stream.write(b"DATA")
        stream.write_uint(len(data) - len(pointer.pad))
        stream.write(data)
        # ovl ignores the padding of the last wem
        instance.size_for_ovl = stream.tell() - len(pointer.pad)
        print("AUX size for OVL", instance.size_for_ovl)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		cls.read_fields(stream, instance)
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		cls.write_fields(stream, instance)
		return instance
