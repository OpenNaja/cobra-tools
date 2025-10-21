from generated.array import Array
from generated.formats.particleeffect.structs.Effect import Effect
from generated.formats.particleeffect.structs.ParticleEffectRoot import ParticleEffectRoot
from modules.formats.BaseFormat import MimeVersionedLoader


class ParticleEffetLoader(MimeVersionedLoader):
	target_class = ParticleEffectRoot
	extension = ".particleeffect"

	def create(self, file_path):
		super().create(file_path)
		fp = f"{file_path}buffer"
		with open(fp, "rb") as f:
			self.create_data_entry((f.read(),))
			for f_name, f_type, (arg, template), _ in self.header._get_filtered_attribute_list(self.header):
				if f_name.startswith("effect"):
					field = self.header.get_field(self.header, f_name)
					if template is not Effect:
						# Array.from_stream(stream, loader.context, 0, None, (len(loader.children),), ManiInfo)
						f.seek(field.offset)
						effects = Array.from_stream(f, self.context, 0, None, field.count, template)
						print(effects)

	def extract(self, out_dir):
		paths = list(super().extract(out_dir))
		fp = f"{paths[0]}buffer"
		paths.append(fp)
		with open(fp, "wb") as f:
			for i, b in enumerate(self.data_entry.buffer_datas):
				f.write(b)
		return paths
