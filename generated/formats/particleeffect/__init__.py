from io import BytesIO
import os
import time
import logging

from generated.formats.ovl_base import OvlContext
from generated.formats.particleeffect.compounds.ParticleEffectRoot import ParticleEffectRoot
from generated.io import IoFile

logging.basicConfig(level=logging.DEBUG)

class ParticleEffectFile(ParticleEffectRoot, IoFile):

	def __init__(self, ):
		pass

	def load(self, filepath, read_bytes=False, read_editable=False):
		start_time = time.time()
		self.filepath = filepath
		self._context = OvlContext()
		self.dir, self.name = os.path.split(os.path.normpath(filepath))
		self.read_editable = read_editable
		logging.debug(f"Reading {self.filepath}")
		self.particleeffect = ParticleEffectRoot.from_xml_file(self.filepath, self._context)

