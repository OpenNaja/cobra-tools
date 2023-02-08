from generated.formats.particleeffect.compounds.ParticleEffectRoot import ParticleEffectRoot
from modules.formats.BaseFormat import MemStructLoader


class ParticleEffetLoader(MemStructLoader):
	target_class = ParticleEffectRoot
	extension = ".particleeffect"

	def create(self, file_path):
		super().create(file_path)
		fp = f"{file_path}buffer"
		with open(fp, "rb") as f:
			self.create_data_entry((f.read(),))

	def extract(self, out_dir):
		paths = list(super().extract(out_dir))
		fp = f"{paths[0]}buffer"
		paths.append(fp)
		with open(fp, "wb") as f:
			for i, b in enumerate(self.data_entry.buffer_datas):
				f.write(b)
		return paths
